# Telegram-Recorder-Audio
A Python script for recording audio on Android using Termux and automatically sending the recordings to a Telegram chat via a bot.

# Telegram Audio Recorder for Termux

This project is a Python script designed to **record audio from an Android device using Termux** and **automatically send the recordings to a Telegram chat** via a Telegram bot.
The script continuously records short audio clips and uploads them to Telegram.

## ⚠️ Legal Notice ⚠️

Recording audio without the consent of all parties may be illegal in your country.  
This project is provided **for educational and personal use only**.  
You are fully responsible for how you use it.

## Requirements

- Android smartphone
- Termux (latest version)
- Telegram account
- Telegram Bot Token
- Internet connection

## Termux Setup

### Install Termux
Download Termux from my Gdrive:
<pre>https://drive.google.com/file/d/1Yzu1tpzvVSmfOvMsWI_7uttajqTySS-z/view?usp=drive_link</pre>

# Update Termux
Open Termux and run:
<pre>pkg update && pkg upgrade</pre>

# Install required packages:
<pre>pkg install python ffmpeg portaudio git -y</pre>

# Install Python dependencies
<pre>pip install pyaudio requests</pre>
If pyaudio fails to install:
<pre>pip install --no-binary :all: pyaudio</pre>

# Telegram Bot Setup
Create a Telegram bot
Open Telegram
Search for 
<pre>@BotFather</pre>
<pre>/start</pre>
<pre>/newbot</pre>
Copy the BOT TOKEN

# Get your Chat ID
Start a chat with your bot
Send any message to it
Open in browser (replace TOKEN):
<pre>https://api.telegram.org/bot<TOKEN>/getUpdates</pre>
Copy your chat.id

# Script Configuration

Open the Python script and replace:
<pre>TELEGRAM_TOKEN = "123456789:AAABBBcccDDD_EEEfffGGG"
CHAT_ID = "1234567890"
</pre>
with your real values.

Storage Location

# Audio files are saved in:
<pre>/storage/emulated/0/MyAudio</pre>

# How to Run
From Termux, navigate to the script folder:
<pre>cd ~/telegram-audio-recorder</pre>
Run the script:
<pre>python recorder.py</pre>

# 🔁 How It Works

Records 1 minute of audio
Sends a Telegram notification at 95% progress
Uploads the audio file to Telegram
Waits 1 second
Repeats indefinitely
Stop the script with:
<pre>CTRL + C</pre>

# 📊 Notes & Recommendations

WAV files are large (~5–6 MB per minute)
Continuous use consumes battery and data
Consider converting to MP3 for lower bandwidth
Do NOT expose your Telegram bot token publicly

# 🔐 Security Warning
Never commit your real Telegram token to a public repository.
Use environment variables or a .env file for production use.

# 📌 Disclaimer
This software is provided "as is", without warranty of any kind.
The author is not responsible for misuse.

# ⭐ Credits
Developed for educational purposes using:
Python
PyAudio
Telegram Bot API
Termux (Android)
