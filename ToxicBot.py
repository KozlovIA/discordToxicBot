import func
import discord
from discord.ext import commands
from discord.utils import get
import json
import requests
from youtube_dl import YoutubeDL
from asyncio import sleep
import time

bot = commands.Bot(command_prefix='!') #define command decorators

@bot.event
async def on_ready():
    print('Logged on!')


#@bot.command()     # комментарий, чтобы функция on_message не работала
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))
    if str(message.author) == "ToxicBot#7701":
        return
    if '{0.content}'.format(message) == 'Hi':
        await message.channel.send('Hello!')


@bot.command()
async def online(ctx):
    await ctx.send("Я живее всех мертвых!")

@bot.command()
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Random Fox') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed



@bot.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Токсичность залетает в беседу: {channel}')

@bot.command(pass_context=True)
async def leave(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f'Токсичность покидает безмятежную беседу : {channel}')
    else:
        voice = await channel.connect()



YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


@bot.command()
async def play(ctx, *, args):

    if ('https://' in args) == False:
        args = func.search_URL(args)[0]

    global vc

    try:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
    except:
        print('Уже подключен или не удалось подключиться')

    if vc.is_playing():
        await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается.')

    else:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(args, download=False)

        URL = info['formats'][0]['url']

        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\bin\\ffmpeg.exe", source = URL, **FFMPEG_OPTIONS))
                
        while vc.is_playing():
            await sleep(1)
        if not vc.is_paused():
            await vc.disconnect()

@bot.command()
async def pause(ctx):
    if vc.is_playing():
        vc.pause()
    elif vc.is_paused():
        vc.resume()
        
@bot.command()
async def stop(ctx):
    if vc.is_playing() or vc.is_pause():
        vc.stop()


bot.run('ODY1Njg3NzM5Mjg1NzY2MjA1.YPHoiA.fCz4Jr235GTFBhxtSOJc55UxjNo')
