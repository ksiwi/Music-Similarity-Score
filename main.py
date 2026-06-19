from utils import download_audio_from_youtube

def main():
    youtube_url = 'https://www.youtube.com/watch?v=7a8GkEgPhlA&list=RDcIxGUAnj46U&index=7'
    music_file_path = 'music.mp3'

    download_audio_from_youtube(youtube_url, 'youtube_audio')

if __name__ == '__main__':
    main()