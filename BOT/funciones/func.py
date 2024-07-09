from pytube import YouTube
from youtube_search import YoutubeSearch
import os
from moviepy.editor import *
import json
import uuid  # Para generar un ID único para cada descarga
import threading

def search_download_return_url(query, folder_name):
    try:
        # Buscar video por texto
        results = YoutubeSearch(query, max_results=1).to_json()
        results_dict = json.loads(results)
        
        if results_dict['videos']:
            video_info = results_dict['videos'][0]
            video_url = f"https://www.youtube.com{video_info['url_suffix']}"
            
            # Descargar y convertir a MP3
            yt = YouTube(video_url)
            video = yt.streams.filter(only_audio=True).first()
            video_file = video.download(filename='temp')

            if os.path.exists(video_file):
                mp3_file = f'{uuid.uuid4()}.mp3'  # Nombre único para el archivo MP3
                dest_folder = f'./BOT/descargas/{folder_name}/'  # Carpeta de destino especificada

                os.makedirs(dest_folder, exist_ok=True)  # Crear la carpeta si no existe

                # Convertir y guardar el archivo MP3 en la carpeta de destino
                video_clip = AudioFileClip(video_file)
                video_clip.write_audiofile(os.path.join(dest_folder, mp3_file))

                # Eliminar el archivo de video temporal
                os.remove(video_file)

                # Programar la eliminación del archivo MP3 después de 10 minutos
                def eliminar_archivo_mp3(mp3_path):
                    try:
                        os.remove(mp3_path)
                        print(f"Archivo MP3 eliminado: {mp3_path}")
                    except Exception as e:
                        print(f"No se pudo eliminar el archivo MP3: {e}")

                mp3_path = os.path.join(dest_folder, mp3_file)
                timer = threading.Timer(600, eliminar_archivo_mp3, args=[mp3_path])
                timer.start()

                # Devolver la ruta del archivo MP3 descargado
                return os.path.join(dest_folder, mp3_file)
            else:
                print(f"Error: No se pudo descargar el video desde {video_url}")
                return None
        else:
            print(f"No se encontraron resultados para: {query}")
            return None

    except Exception as e:
        print(f"Error durante la búsqueda/descarga: {e}")
        return None

    







