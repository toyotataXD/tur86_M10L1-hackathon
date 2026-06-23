import discord
from discord.ext import commands
from discord_token import TOKEN
from ai_token import GROQ_TOKEN
import requests
import threading
import pyttsx3

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

def ai_reply(text):                 # AI Kurulum
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": text}]
    }
    r = requests.post(url, json=data, headers=headers)
    try:
        return r.json()["choices"][0]["message"]["content"]
    except:
        return r.text

def tts_generate(text):
    def run_tts():
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.save_to_file(text, "ai_voice.mp3")
        engine.runAndWait()
        engine.stop()

    t = threading.Thread(target=run_tts)
    t.start()
    t.join()
    return "ai_voice.mp3"

@bot.event
async def on_ready():
    print(f"{bot.user} is working")     

@bot.command()             # Sesli kanala katılma komutu
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("I joined the voice channel")
    else:
        await ctx.send("You must join a voice channel first")

@bot.command()
async def ai(ctx, *, text=None):
    if text is None:
        text = "..."
    reply = ai_reply(text)
    await ctx.reply(reply)

@bot.command()
async def vci(ctx, *, text=None):
    if text is None:
        text = "..."

    reply = ai_reply(text)
    await ctx.reply(reply)

    vc = ctx.voice_client

    if vc is None:
        await ctx.send("Im not in a voice channel. Use !join to add me")
        return

    if not vc.is_connected():
        await ctx.send("Im not in a voice channel, use !join to add me.")
        return

    audio_file = tts_generate(reply)

    audio = discord.FFmpegPCMAudio(
        executable=r"C:\Users\KILIC\Downloads\ffmpeg-2026-06-15-git-44d082edc8-full_build\ffmpeg-2026-06-15-git-44d082edc8-full_build\bin\ffmpeg.exe",
        source=audio_file
    )

    if not vc.is_playing():
        vc.play(audio)


bot.run(TOKEN)


### Hocam benim discord botum sesli bi yapay zeka botu olcaktı, botta tek bi hata var o da kodun çalışmasına engel değil ama sesli kanala katıldığında ve TTS özelliğini kullanmaya çalıştığında, bot sesinin karşı kullanıcıya gitmemesi. Bu problem çözülmezse bot sadece işlevsellik kaybeder. zaten sesli olmadan konuşmak için ayrı bi komutta yaptım. Sorunu yapay zekadan yardım alarak çözmeye çalıştım ama hiç bir türlü olmadı