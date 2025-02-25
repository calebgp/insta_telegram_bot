import os
import instaloader
import requests

def get_final_url(share_link):
    try:
        response = requests.get(share_link, allow_redirects=True)
        if response.status_code == 200:
            return response.url
        else:
            return f"Error: Received status code {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"

def download_video(url):
    if 'share' in url:
        url = get_final_url(url)
    
    shortcode = url.split('/')[-2]
    print(shortcode)

    L = instaloader.Instaloader(
        filename_pattern='video',
        dirname_pattern='videos/{shortcode}',
        download_pictures=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        resume_prefix='description'
    )
    
    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=f'{shortcode}')
        filepath = f"{os.getcwd()}/videos/{shortcode}/video.mp4"
        return filepath
    except Exception as e:
        print(f"Erro ao baixar o vídeo: {e}")
        return None

link = input('Digite o link do vídeo: ')
destination = download_video(link)

if destination:
    print(f'Vídeo baixado com sucesso! Salvo em: {destination}')
else:
    print('Falha ao baixar o vídeo.')
