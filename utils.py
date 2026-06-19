import numpy as np
import yt_dlp as youtube_dl
import librosa
import yt_dlp as youtube_dl
from urllib.parse import urlparse, parse_qs
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

#Used to ge thte correct URL ebcause sometimes they come in palylists or mixtapes, which makes it difficult for yt_dlp to handle
def clean_url(video_url):
    parsed = urlparse(video_url)
    video_id = parse_qs(parsed.query).get('v')
    #The v is the marker for the video id

    if(video_id):
        return f"https://www.youtube.com/watch?v={video_id[0]}"
    
    return video_url


def download_audio_from_youtube(video_url, output_path):

    video_url = clean_url(video_url)
    
    options = {

        'format': 'bestaudio/best',
        #Says that the best quality option of the video should be downloaded
        'postprocessors': [{

            #Converts into mp3 format

            'key': 'FFmpegExtractAudio',
            #FFmpeg is the intended tool to take the audio
            'preferredcodec': 'mp3',
            #Makes the file into mp3
            'preferredquality': '192'
            #192 means 192kbps, which is the sound quality we want without having too big of a file size

        }],
        'outtmpl': output_path,
        #The downloaded file will be put into output_path
        'ffmpeg_location': r'C:\ffmpeg\bin',
        'js_runtimes': {
            'deno': {'path': r'C:\Users\William\AppData\Roaming\npm\deno.cmd'}
        },

    }

    with youtube_dl.YoutubeDL(options) as ydl:

        try:
            ydl.download([video_url])
        except Exception as e:
            print(f'Error was: {e}')

