from flask import Flask, request, render_template, jsonify
from pytube import YouTube, Playlist
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)

progress = 0

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    playlist_url = request.form['playlist_url']
    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    os.makedirs(download_folder, exist_ok=True)
    download_playlist_to_mp3(playlist_url, download_folder)
    return 'Playlist downloaded and converted to MP3 successfully!'
  return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
  playlist_url = request.json['playlistUrl']
  download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
  os.makedirs(download_folder, exist_ok=True)
  download_playlist_to_mp3(playlist_url, download_folder)
  return jsonify({'message': 'Playlist downloaded and converted to MP3 successfully!'})

@app.route('/progress', methods=['GET'])
def progress():
  global progress
  return jsonify({'progress': progress})

def get_progress():
  global progress
  return progress

def download_playlist_to_mp3(playlist_url, download_folder):
  global progress
  playlist = Playlist(playlist_url)
  total_videos = len(playlist.video_urls)
  for i, video_url in enumerate(playlist.video_urls):
    yt = YouTube(video_url)
    stream = yt.streams.get_highest_resolution()
    print(f"Downloading: {yt.title}")
    temp_file_path = stream.download(filename='temp_video.mp4', output_path=download_folder)
    video = VideoFileClip(temp_file_path)
    title = yt.title
    title = "".join(x for x in title if x.isalnum() or x in "._- ")
    audio_file_path = os.path.join(download_folder, f"{title}.mp3")
    video.audio.write_audiofile(audio_file_path)
    print(f"Downloaded and converted to MP3: {audio_file_path}")
    video.close()  # Close the VideoFileClip object
    os.remove(temp_file_path)
    progress = int((i + 1) / total_videos * 100)

if __name__ == '__main__':
  app.run(debug=True)