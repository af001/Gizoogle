#!/bin/bash

# Create a Google Cloud Platform project and credential file
echo "[+] Create a project on the Google Cloud Platform"
echo "[+] Create a service account key (json): APIs & Services --> Credentials"
echo "[+] Put the key in your project path."
read -p "[+] Enter the absolute path for your key: " KEY
export GOOGLE_APPLICATION_CREDENTIALS=$KEY
echo
echo "Initializing gsutil and creating buckets with the appropriate permissions"
gcloud init
echo
VIDEO=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)
AUDIO=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)
IMAGE=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)
DOCUMENT=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)
gsutil mb gs://video_$VIDEO
gsutil mb gs://audio_$AUDIO
gsutil mb gs://image_$IMAGE
gsutil mb gs://document_$DOCUMENT
echo
echo "[+] Show the buckets"
gsutil ls
sleep 2
echo
echo "[+] Changing permissions to world readable for each bucket"
gsutil iam ch allUsers:objectViewer gs://video_$VIDEO
gsutil iam ch allUsers:objectViewer gs://audio_$AUDIO
gsutil iam ch allUsers:objectViewer gs://image_$IMAGE
gsutil iam ch allUsers:objectViewer gs://document_$DOCUMENT
echo
echo "[+] Setting lifecycle to delete files older than 10 days in each bucket"
gsutil lifecycle set bucket_config.json gs://video_$VIDEO
gsutil lifecycle set bucket_config.json gs://audio_$AUDIO
gsutil lifecycle set bucket_config.json gs://image_$IMAGE
gsutil lifecycle set bucket_config.json gs://document_$DOCUMENT
echo 
echo
echo "[+] Usage: python2.7 gizoogle.py"
echo "[+] Terminal Usage: help"
