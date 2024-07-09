from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from threading import Thread
import bot

load_dotenv()

app = FastAPI()
bot_client = bot.bot
bot_thread = None

class Token(BaseModel):
    token: str

class VoiceChannelRequest(BaseModel):
    user_id: int
    guild_id: int
    channel_id: int

@app.post("/start-bot")
async def start_bot(token: Token):
    global bot_thread
    if bot_thread and bot_thread.is_alive():
        raise HTTPException(status_code=400, detail="Bot ya está corriendo")
    
    bot_thread = Thread(target=bot.run_bot, args=(token.token,))
    bot_thread.start()
    return {"message": "Bot iniciado"}

@app.post("/join-voice")
async def join_voice(request: VoiceChannelRequest):
    if not bot.bot.is_ready():
        raise HTTPException(status_code=400, detail="Bot no está listo")
    
    bot_client = bot.bot
    await bot_client.join_voice_channel(request.user_id, request.guild_id, request.channel_id)
    return {"message": "Intentando unir al canal de voz"}

@app.post("/play-music")
async def play_music():
    if not bot_client.is_ready():
        raise HTTPException(status_code=400, detail="Bot is not ready")
    
    await bot_client.play_music("azul - zoe", "123")
    return {"message": "Trying to play music"}


@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API para controlar el bot de Discord"}



