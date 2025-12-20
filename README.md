# Telegram-Recorder Audio
A Python script to record audio continuously in 60-second chunks on Android using Termux, automatically sending recordings to Telegram via curl.

# Features
Records 60-second audio chunks continuously.
Sends Telegram notification 10 seconds before each recording finishes.

Automatically sends recorded M4A files to Telegram.
Pauses 1 second between recordings.
Stops automatically when storage is low or manually with CTRL+C.
Fully compatible with Termux on Android.

# Requirements
# Termux (from F-Droid)
Install Termux from the official F-Droid repository:
https://f-droid.org/packages/com.termux/
Avoid downloading APKs from untrusted sources. The Play Store version is outdated.

# Termux:API (from F-Droid)
Install Termux:API to access microphone, notifications, and other device features:
https://f-droid.org/packages/com.termux.api/
Enable storage access:
<pre>termux-setup-storage</pre>

# Python 3
Install Python in Termux:
<pre>pkg install python</pre>

# curl
Used to send files to Telegram:
<pre>pkg install curl</pre>

# FFmpeg
Install FFmpeg for audio conversion:
<pre>pkg install ffmpeg </pre>
For this script, conversion is optional because it sends M4A directly.

# Create directory:
<pre>mkdir -p /storage/emulated/0/MyAudio</pre>

# Edit record.py with your Telegram credentials: 
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

Records audio in 60-second chunks.
Sends a Telegram message 10 seconds before each recording ends.
Automatically sends the audio file to Telegram.
Pauses 1 second between recordings.
Stops with CTRL+C or if storage is low.

# Folder structure
/storage/emulated/0/MyAudio – recorded audio files (M4A).

# Notes & Tips
Make sure your Telegram bot token and chat ID are correct.
Ensure storage permissions are granted (termux-setup-storage).
Monitor available storage to avoid interruptions.
Files are sent via curl, ensuring compatibility with Telegram.

# Optional
Enable wake lock to prevent the device from sleeping during long recordings:

<pre>termux-wake-lock </pre>

Add Android notifications (requires termux-notification) for visual feedback:

<pre>pkg install termux-tools </pre>
