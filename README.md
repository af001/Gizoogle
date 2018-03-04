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
chmod +x install.sh initialize.sh
sudo ./install.sh
sudo ./initialize.sh
```

1. Follow the instructions on the screen after running the ```sudo ./install.sh```
```bash
Do you want to help improve the Google Cloud SDK(Y/n)? n

Installation directory (this will create a google-cloud-sdk subdirectory) (/root): /home/devnet/Google

Modify profile
Do you want to continue (Y/n)? y
Enter a path to an rc file to update, or leave black to use [/root/.bashrc]: /home/devnet/.bashrc
```
2. Once the ```sudo ./install.sh``` script finishes, run the ```sudo ./initialize.sh``` script to set up your Google Cloud Platform storage buckets.

#### Modify the modules/Config.py python script to include your project specific information. Your bucket names should be output to the screen after running the ```bash sudo ./initialize.sh``` script. If they are not, run ```bash gsutil ls```
```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/devnet/Google/key.json" # Change this to your key.json

PROJECT_ID = 'my-project-212121' # Change this to your project-ID

IMAGE_STORAGE_BUCKET = 'image_dump' # Change this to your image bucket
AUDIO_STORAGE_BUCKET = 'speech_dump' # Change this to your speech bucket
DOCUMENT_STORAGE_BUCKET = 'document_dump' # Change this to your document bucket
VIDEO_STORAGE_BUCKET = 'video_dump' # Change this to your video bucket
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
lang
lang Arabic
translate /home/dev/russian.txt
audio en-US /home/dev/audio.mp3
audio ru-RU gs://audio_bucket/audio.mp3
image https://mysite.com/file.jpeg
image /home/dev/file.png
video en-US /home/dev/video.mp4           # use mp4 for best results
video ru-RU gs://video_bucket/video.mp4
```
#### In Development:
1. Add autodetect file format and analyze
2. Store files, translations, and analysis in BigTable
3. Add query feature to query analyzed files
4. Remove stopwords from translations; determine key words and store in BigTable -> link to files in buckets
5. Integrate NLP and custom ML algorithms
