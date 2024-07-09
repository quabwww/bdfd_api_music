import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from BOT.funciones.func import search_download_return_url
load_dotenv()

class BotClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents().all())

    async def on_ready(self):
        print(f'Bot conectado como {self.user}')

    async def join_voice_channel(self, user_id, guild_id, channel_id):
        guild = self.get_guild(guild_id)
        if not guild:
            raise commands.CommandError(f"Guild {guild_id} no encontrado")
            
        
        member = guild.get_member(user_id)
        if not member:
            raise commands.CommandError(f"Miembro {user_id} no encontrado en el guild")
            

        voice_channel = guild.get_channel(channel_id)
        if not voice_channel or not isinstance(voice_channel, discord.VoiceChannel):
            raise commands.CommandError(f"Canal {channel_id} no es un canal de voz válido")

        if member in voice_channel.members:
            await voice_channel.connect()
            print(f"Bot se unió al canal de voz {voice_channel.name}")
        else:
            
            raise commands.CommandError(f"Miembro {user_id} no está en el canal de voz {channel_id}")

    async def play_music(self, music, folder):
        try:
            # Llamar a la función asíncrona de búsqueda y descarga de música
            mp3_path = await search_download_return_url(music, folder)

            # Obtener el cliente de voz actual del bot
            voice_client = discord.utils.get(self.voice_clients)

            # Verificar si el bot está conectado a un canal de voz
            if not voice_client:
                raise commands.CommandError("Bot is not in a voice channel.")

            # Verificar si el archivo MP3 existe
            if not os.path.exists(mp3_path):
                raise commands.CommandError(f"File {mp3_path} not found.")
            
            voice_client.play(discord.FFmpegPCMAudio(mp3_path), after=lambda e: print(f"Player error: {e}") if e else None)

        # Aquí implementa la lógica para reproducir el archivo MP3 en el canal de voz
        # Por ejemplo, puedes usar voice_client.play() para reproducir el archivo

        except commands.CommandError as e:
        # Capturar y manejar errores específicos de comandos
            print(f"Error executing play_music command: {e}")

        except Exception as e:
        # Capturar cualquier otra excepción inesperada
            print(f"Unexpected error during play_music: {e}")

bot = BotClient()

def run_bot(token):
    bot.run(token)
