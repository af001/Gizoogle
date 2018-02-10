# Gizoogle
Experimentation with Google Cloud APIs 

#### Create a new project under the Google Cloud Platform Console


#### Modify the python script to include your project specific information
```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/dev/key.json" # Change this to your key.json

IMAGE_STORAGE_BUCKET = 'image_dump' # Change this to your image bucket
AUDIO_STORAGE_BUCKET = 'speech_dump' # Change this to your speech bucket
DOCUMENT_STORAGE_BUCKET = 'document_dump' # Change this to your document bucket
VIDEO_STORAGE_BUCKET = 'video_dump' # Change this to your video bucket
PROJECT_ID = 'analysis-283736' # Change this to your project-ID
```



