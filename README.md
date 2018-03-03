# Gizoogle
Experimentation with Google Cloud APIs. This is experimental and is only intended for educational purposes. Code is provided as is. If you are interested in modifying the code, send a pull request. 

#### Create a new project under the Google Cloud Platform Console
Note: The gsutils will be installed with the install script.
1. Setup a project: https://cloud.google.com/dataproc/docs/guides/setup-project
2. Take note of your project id
3. Enable the APIS: Vision, VideoIntelligence, Speech, Translation, Storage
4. Create a service account key and download to your computer
5. In your project console, select IAM & admin and verify your service key account is a member of 'project owner'

#### Download the repo and install dependencies 
```bash
git clone https://github.com/af001/Gizoogle.git
cd Gizoogle
chmod +x install.sh
chmod +x initialize.sh
sudo ./install.sh
sudo ./initialize.sh
```

1. Follow the instructions on the screen after running the ```bash sudo ./install.sh```
2. At the end of the script, there are a number of additional commands you must run to setup your Google Cloud Buckets

The following commands will be provided at the end of the script:

```bash
# Initialize gsutil; provide your project id when asked
gsutil init

# Create 4 new buckets - must have unique names
gsutil mb gs://<a_video_bucket_name>
gsutil mb gs://<a_audio_bucket_name>
gsutil mb gs://<a_image_bucket_name>
gsutil mb gs://<a_document_bucket_name>

# Show the buckets
gsutil ls

# Change permissions to world readable for each bucket
gsutil iam ch allUsers:objectViewer gs://<video_bucket_name>
gsutil iam ch allUsers:objectViewer gs://<audio_bucket_name>
gsutil iam ch allUsers:objectViewer gs://<image_bucket_name>
gsutil iam ch allUsers:objectViewer gs://<document_bucket_name>

# Set lifecycle to delete files older than 10 days in each bucket
gsutil lifecycle set bucket_config.json gs://<video_bucket_name>
gsutil lifecycle set bucket_config.json gs://<audio_bucket_name>
gsutil lifecycle set bucket_config.json gs://<image_bucket_name>
gsutil lifecycle set bucket_config.json gs://<document_bucket_name>
```

#### Modify the modules/Config.py python script to include your project specific information
```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/dev/key.json" # Change this to your key.json

IMAGE_STORAGE_BUCKET = 'image_dump' # Change this to your image bucket
AUDIO_STORAGE_BUCKET = 'speech_dump' # Change this to your speech bucket
DOCUMENT_STORAGE_BUCKET = 'document_dump' # Change this to your document bucket
VIDEO_STORAGE_BUCKET = 'video_dump' # Change this to your video bucket
PROJECT_ID = 'analysis-283736' # Change this to your project-ID
```

#### Usage
```bash
python2.7 gizoogle.py
```

#### Terminal Usage:
```python
# Show help menu
help

# Show usage for each command
help [translate, video, audio, image, lang]

# Examples
translate /home/dev/russian.txt
audio en-US /home/dev/audio.mp3
audio ru-RU gs://audio_bucket/audio.mp3
image https://mysite.com/file.jpeg
image /home/dev/file.png
lang
lang Arabic
video en-US /home/dev/video.mp4           # use mp4 for best results
video ru-RU gs://video_bucket/video.mp4
```
#### In Development:
1. Add autodetect file format and analyze
2. Store files, translations, and analysis in BigTable
3. Add query feature to query analyzed files
4. Remove stopwords from translations; determine key words and store in BigTable -> link to files in buckets
5. Integrate NLP and custom ML algorithms
6. Do video analysis, convert to audio, translate, transcribe 


