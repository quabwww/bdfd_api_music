import os
import yt_dlp
from youtube_search import YoutubeSearch
from pydub import AudioSegment

class YTLOGGER(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

async def get_most_recent_file_in_folder(folder_path):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    if not files:
        return None
    
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

async def search_download_and_convert_to_mp3(query_text, path):
    try:
        # Search for video using youtube_search
        results = YoutubeSearch(query_text, max_results=1).to_dict()
        if not results:
            raise ValueError("No video found for the given query.")
        
        video_id = results[0]['id']
        video_title = results[0]['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'logger': YTLOGGER(),
            'outtmpl': os.path.join(f"BOT/descargas/{path}", '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            original_filename_webm = ydl.prepare_filename(info_dict)
            
            # Convert to MP3 using pydub
            audio = AudioSegment.from_file(original_filename_webm)
            finalname_mp3 = os.path.join(path, f'{video_title}.mp3')
            audio.export(finalname_mp3, format="mp3")
        
        # Get the most recent file in the specified path
        first_file = get_most_recent_file_in_folder(path)
        
        # Return paths to both webm and mp3 files, and the path to the first file (if found)
        return finalname_mp3, original_filename_webm, first_file
    
    except Exception as e:
        # Aquí manejas cualquier excepción que ocurra sin imprimir el mensaje en la consola.
        # Puedes registrar el error o simplemente ignorarlo si lo prefieres.
        return None, None, None  # Devuelve None en caso de error




