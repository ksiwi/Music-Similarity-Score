from utils import download_audio_from_youtube, similarity_score_cosine, extract_features

def main():
    youtube_url = 'https://www.youtube.com/watch?v=cIxGUAnj46U&list=RDcIxGUAnj46U&start_radio=1&pp=ygUNbGEgY2FtcGFuZWxsYaAHAQ%3D%3D'
    input_url = 'https://www.youtube.com/watch?v=hKILwVH_MdM&list=RDcIxGUAnj46U&index=8'

    #download_audio_from_youtube(youtube_url, 'youtube_audio')
    download_audio_from_youtube(input_url, 'input_audio')
    
    print(similarity_score_cosine('youtube_audio.mp3', 'input_audio.mp3'))

if __name__ == '__main__':
    main()