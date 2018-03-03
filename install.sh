#!/bin/bash

## GizOOgle Insatll Script
## Rev. 1.0a

# Update linux
apt-get update && apt-get -y upgrade
apt-get -y install python python-pip ffmpeg build-essential curl

# Install Python packages --> change to requirments.txt
echo "[+] Installing Python packages..."
pip install --upgrade setuptools google-cloud-speech google-cloud-videointelligence google-cloud-vision google-cloud-storage google-cloud-translate pyfiglet Werkzeug ffmpy six

# Verify ffmpeg and python are installed and in your path
echo
echo "[+] You should see ffmpeg and python2.7 installed!!!"
python --version
ffmpeg -version | grep ffmpeg
echo

# Install gsutil command line tools and install
echo "[+] Downloading and installing gsutils"
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

