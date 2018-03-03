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

# Create a Google Cloud Platform project and credential file
echo "[+] Create a project on the Google Cloud Platform"
echo "[+] Create a service account key (json): APIs & Services --> Credentials"
echo "[+] Put the key in your project path"
echo 

# Install gsutil command line tools and install
echo "[+] Downloading and installing gsutils"
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
echo
echo "[+] Run the following commands from the terminal:"

# Initialize gsutil and create buckets with the appropriate permissions
echo "# Initialize gsutil"
echo "gsutil init"
echo
echo "# Create 4 new buckets - must have unique names"
echo "gsutil mb gs://<a_video_bucket_name>"
echo "gsutil mb gs://<a_audio_bucket_name>"
echo "gsutil mb gs://<a_image_bucket_name>"
echo "gsutil mb gs://<a_document_bucket_name>"
echo
echo "# Show the buckets"
echo "gsutil ls"
echo
echo "# Change permissions to world readable for each bucket"
echo "gsutil iam ch allUsers:objectViewer gs://<video_bucket_name>"
echo "gsutil iam ch allUsers:objectViewer gs://<audio_bucket_name>"
echo "gsutil iam ch allUsers:objectViewer gs://<image_bucket_name>"
echo "gsutil iam ch allUsers:objectViewer gs://<document_bucket_name>"
echo
echo "# Set lifecycle to delete files older than 10 days in each bucket"
echo "gsutil lifecycle set bucket_config.json gs://<video_bucket_name>"
echo "gsutil lifecycle set bucket_config.json gs://<audio_bucket_name>"
echo "gsutil lifecycle set bucket_config.json gs://<image_bucket_name>"
echo "gsutil lifecycle set bucket_config.json gs://<document_bucket_name>"
echo 
echo
echo "[+] Usage: python2.7 gizoogle.py"
echo "[+] Terminal Usage: help"
