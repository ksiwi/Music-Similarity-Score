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

#takes all the features from an mp3 file
def extract_features(audio_path):
    
    #y is the audio array, and sr is the sampling rate of the file
    y, sr = librosa.load(audio_path)

    #MFCC are Mel-Frequency Cepstral Coefficients (changes audio to numerical format), n_mfcc = 20 is the amount of coefficients to take
    mfccs = librosa.feature.mfcc(y = y, sr = sr, n_mfcc = 20)

    #Chroma is the different pitches in audio, the code gives a 12 dimensional vector that represent the 12 notes in an octave
    chroma = librosa.feature.chroma_stft(y = y, sr = sr)

    #RMS is the Root Mean Square Energy that measures magnitude of the audio signals
    rms = librosa.feature.rms(y = y)

    #Spectral contrast measures in amplitude between highest and lowest parts of an audio signal (Splits up audio into different frequency bands and measures the contrast between these bands, and there are 7 vectors which represent the frequency bands)
    spectral_contrast = librosa.feature.spectral_contrast(y = y, sr = sr)

    mfccs_mean = np.mean(mfccs, axis = 1)
    mfccs_std = np.std(mfccs, axis = 1)
    chroma_mean = np.mean(chroma, axis = 1)
    chroma_std = np.std(chroma, axis = 1)
    rms_mean = np.mean(rms, axis = 1)
    rms_std = np.std(rms, axis = 1)
    spectral_contrast_mean = np.mean(spectral_contrast, axis = 1)
    spectral_contrast_std = np.mean(spectral_contrast, axis = 1)

    #Takes in all the notable data and puts it into a vector
    feature_vector = np.concatenate([

        mfccs_mean, mfccs_std,
        chroma_mean, chroma_std,
        rms_mean, rms_std,
        spectral_contrast_mean, spectral_contrast_std

    ])

    #Normalizes the vector (Makes it into magnitude 1)
    normalized_feature_vector = normalize(feature_vector.reshape(1, -1))

    #Turns the 8d array into 1d
    return normalized_feature_vector.flatten()
