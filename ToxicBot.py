import func
import discord
from discord.ext import commands
from discord.utils import get
import json
import requests
from youtube_dl import YoutubeDL
from asyncio import sleep
from bs4 import BeautifulSoup


play_list = []      # лист URL с музыкой
name_list = []      # лист с именами песен

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
    """Узнать у бота онлайн ли он"""
    await ctx.send("Я живее всех мертвых!")

@bot.command()
async def fox(ctx):
    """Команда - загадка"""
    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Random Fox') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed



@bot.command(pass_context=True)
async def join(ctx):
    """Просто присоеденить бота к каналу"""
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
    """Выгнать бота. Может сам выйдешь?"""
    await stop(ctx)
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
async def play(ctx, *, args=None):
    """Начать вопроизведение или добавить песню в плейлист"""

    global vc
    try:
        voice_channel = ctx.message.author.voice.channel    # подключение к каналу
        vc = await voice_channel.connect()
    except:
        print('Уже подключен или не удалось подключиться')

    if args != None:         # поиск песни или названия
        if ('https://' in args) == False:   
            p_temp, n_temp = func.search_URL(args)
        else:
            clip = requests.get(args)   # достаем имя на ютубе по ссылке
            inspect = BeautifulSoup(clip.content, "html.parser")
            yt_title = inspect.find_all("meta", property="og:title")
            for concatMusic1 in yt_title:
                pass
            p_temp, n_temp = args, concatMusic1['content']

        await ctx.send(f'{n_temp}, добавлена в плейлист.')
        play_list.append(p_temp)
        name_list.append(n_temp)

    if len(play_list) == 0:
        print("Плейлист пуст")
        return

    while vc.is_playing():
        await sleep(1)

    if not vc.is_paused():
        if len(play_list) > 1:
            play_list.pop(0)
            name_list.pop(0)

        current_music = play_list[0]
        name_current_music = name_list[0]

        if vc.is_playing():
            await ctx.send(f'{ctx.message.author.mention}, музыка уже проигрывается.')

        else:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(current_music, download=False)

            URL = info['formats'][0]['url']
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\bin\\ffmpeg.exe", source = URL, **FFMPEG_OPTIONS))
            await ctx.send(f'Играем : {name_current_music}')



@bot.command()
async def next(ctx):
    """Следующая композиция в плейлисте"""
    if vc.is_playing() or vc.is_pause():
        vc.stop()
        await play(ctx)


@bot.command()
async def pause(ctx):
    """Приостановить или продолжить воспроизведение музыки"""
    if vc.is_playing():
        vc.pause()
        await ctx.send(f'Пауза в твоей счастливой жизни')
    elif vc.is_paused():
        vc.resume()
        await ctx.send(f'Возращаем радость и страдания')

@bot.command()
async def resume(ctx):
    """Продолжить проигрывание музыки"""
    if vc.is_paused():
        vc.resume()
        await ctx.send(f'Возращаем радость и страдания, какой ты умный, знаешь слово "resume"')
        
@bot.command()
async def stop(ctx):
    """Остановить проигрывание музыки? Себя останови!"""
    if vc.is_playing() or vc.is_pause():
        vc.stop()
        await ctx.send(f'Моя остановочка')


@bot.command()
async def playlist(ctx):
    """Посмотреть плейлист"""
    song_name = ''
    for i in range(len(name_list)):
        song_name += name_list[i] + '\n'
    embed = discord.Embed(color = 0xff9900, title = 'Playlist') # Создание Embed'a
    embed.set_image(url = "https://itc.ua/wp-content/uploads/2019/09/Apple-Music-Android.jpg") # Устанавливаем картинку Embed'a
    embed.add_field(name='Песенки', value=song_name)

    await ctx.send(embed = embed) # Отправляем Embed


bot.run('ODY1Njg3NzM5Mjg1NzY2MjA1.YPHoiA.fCz4Jr235GTFBhxtSOJc55UxjNo')
