import os
import requests
import instaloader
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to get the final URL from a share link
def get_final_url(share_link):
    try:
        response = requests.get(share_link, allow_redirects=True)
        if response.status_code == 200:
            return response.url
        else:
            return f"Error: Received status code {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"

# Function to download video from Instagram
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
        print(f"Error downloading video: {e}")
        return None

# Function to handle messages
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if 'instagram.com' in text:
        video_file = download_video(text)
        if video_file:
            await context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_file, 'rb'))

# Main function
def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")
    application = ApplicationBuilder().token(token).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()