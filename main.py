import os
import logging
import asyncio
import yt_dlp
from dotenv import load_dotenv
from keep_alive import keep_alive
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def download_function(link):
        try:
            ydl_opts = {
                'quiet': True,
                'cookiefile': 'cookies.txt',  # Обязательно нужны cookies для Instagram
                'noplaylist': True,
                'nocheckcertificate': True,  
                'geo_bypass': True,  
                'merge_output_format': 'mp4',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=False)

                # Выбираем лучший mp4-формат со звуком
                best_format = max(
                    (fmt for fmt in info_dict.get('formats', []) 
                    if fmt.get('ext') == 'mp4' and fmt.get('acodec') != 'none'),
                    key=lambda f: f.get('height', 0),
                    default=None
                )

                return {
                    'title': info_dict.get('title', 'Unknown'),
                    'description': info_dict.get('description', ''),
                    'cover_url': info_dict.get('thumbnail', ''),
                    'video_url': best_format.get('url') if best_format else None,
                    'resolution': f"{best_format.get('height')}p" if best_format else "Unknown"
                }
        except Exception as e:
            logging.error(f'Error: {e}')
            print(f'Error: {e}')

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer('Привет! Я Бот который скачивает видео из инстаграм в высшем качестве.\n Отправьте ссылку c Instagram, и я скачаю для вас видео.')

@dp.message()
async def download_video(message: types.Message):
    link = message.text.strip()

    if not 'instagram.com' in link:
        await message.answer('Ссылка должна начинаться с https://instagram.com/')
        return
    
    await message.answer('⌛️')

    result_video = await download_function(link)

    if 'error' in result_video:
        await message.answer('Ошибка в скачивание видео.')
        return

    video_url = result_video['video_url']

    await message.answer_video(video=video_url, 
                               caption='Видео скачано! @nf1downloader_bot')



async def main():
    keep_alive()  # For Heroku deployment
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())