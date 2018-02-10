# Gizoogle
Experimentation with Google Cloud APIs. This is experimental and is only intended for educational purposes. Code is provided as is. If you are interested in modifying the code, send a pull request. 

#### Create a new project under the Google Cloud Platform Console
Note: The gsutils will be installed with the install script.
1. Setup a project: https://cloud.google.com/dataproc/docs/guides/setup-project
2. Take note of your project id
3. Enable the APIS: Vision, VideoIntelligence, Speech, Translation
4. Create a service account key and download to your computer

#### Download the repo and install dependencies 
```bash
git clone 
```

#### Modify the python script to include your project specific information
```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/dev/key.json" # Change this to your key.json

IMAGE_STORAGE_BUCKET = 'image_dump' # Change this to your image bucket
AUDIO_STORAGE_BUCKET = 'speech_dump' # Change this to your speech bucket
DOCUMENT_STORAGE_BUCKET = 'document_dump' # Change this to your document bucket
VIDEO_STORAGE_BUCKET = 'video_dump' # Change this to your video bucket
PROJECT_ID = 'analysis-283736' # Change this to your project-ID
```



