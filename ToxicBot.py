import func
import time
import json
import discord
import requests
import traceback
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
from asyncio import sleep
from bs4 import BeautifulSoup 
from threading import Timer
#from discord import opus
#import opuslib

play_list = []      # лист URL с музыкой
name_list = []      # лист с именами песен 
time_to_leave = 6  # время до выхода бота из канала после окончания плейлиста
global no_music_time    # время начала существования подключенного бота без музыки

intents = discord.Intents.default()
# intents.all()

# bot_intents = ['auto_moderation',
#  'auto_moderation_configuration',
#  'auto_moderation_execution',
#  'bans',
#  'dm_messages',
#  'dm_reactions',
#  'dm_typing',
#  'emojis',
#  'emojis_and_stickers',
#  'guild_messages',
#  'guild_reactions',
#  'guild_scheduled_events',
#  'guild_typing',
#  'guilds',
#  'integrations',
#  'invites',
#  'members',
#  'message_content',
#  'messages',
#  'presences',
#  'reactions',
#  'typing',
#  'value',
#  'voice_states',
#  'webhooks']

# for intent in bot_intents:
#     exec(f"intents.{intent} = True")

intents.message_content = True

# intents.auto_moderation = True
# intents.auto_moderation_configuration = True
# intents.auto_moderation_execution = True
# intents.bans = True
# intents.dm_messages = True
# intents.dm_reactions = True
# intents.dm_typing = True
# intents.emojis = True
# # intents.emojis_and_stickers = True
# intents.guild_messages = True
# intents.guild_reactions = True
# intents.guild_scheduled_events = True
# intents.guild_typing = True
# intents.guilds = True
# intents.integrations = True
# intents.invites = True
# intents.members = True
# intents.message_content = True
# intents.messages = True
# intents.presences = True
# # intents.reactions = True
# # intents.typing = True
# intents.value = True
intents.voice_states = True
# intents.webhooks = True


bot = commands.Bot(command_prefix='!', intents=intents) #define command decorators and bots


@bot.event
async def on_ready():
    print('Logged on!')


@bot.command()     # комментарий, чтобы функция on_message не работала
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))
    if str(message.author) == "ToxicBot#7701":
        return
    if '{0.content}'.format(message) == 'Hi':
        await message.channel.send('Hello!')


@bot.command()
async def online(ctx):
    """Узнать у бота онлайн ли он"""
    await ctx.send("Я живее всех мертвых! :ghost:")

@bot.command()
async def fox(ctx):
    """Команда - загадка"""
    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff9900, title = 'Random Fox :fox:') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed



@bot.command(pass_context=True)
async def join(ctx):
    """Просто присоеденить бота к каналу"""
    try:
        if ~('voice' in globals()):
            global vc
            vc = get(bot.voice_clients, guild = ctx.guild)
        channel = ctx.message.author.voice.channel
        if vc and vc.is_connected():
            await vc.move_to(channel)
        else:
            vc = await channel.connect()
            await ctx.send(f'Токсичность залетает в беседу: {channel} :hugging:')
            timer = Timer(5, await leave, ctx, timer=True)
            timer.start()       # при коннекте запускается таймер для дисконнекта по времени
    except:
        print("join error")


@bot.command(pass_context=True)
async def leave(ctx, timer=False):
    """Выгнать бота. Может сам выйдешь?"""
    """ if timer:
        if ~vc.playing() and ~vc.is_paused():
            no_music_time = time.time()
         """
    await stop(ctx)
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f'Токсичность покидает безмятежную беседу : {channel} :feet:')
    

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

@bot.command()
async def play(ctx, *, args=None):
    """Начать вопроизведение или добавить песню в плейлист"""
    await join(ctx)

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
        await ctx.send(f'{n_temp}, добавлена в плейлист :musical_note:')
        play_list.append(p_temp)
        name_list.append(n_temp)

    if len(play_list) == 0:
        print("Плейлист пуст")
        return

    while vc.is_playing():  #пока музыка играет, ничего не делаем # при добавлении некст песни, запускается этот цикл и ждет, пока отыграет предыдущая
        await sleep(1)
    try:
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
                await ctx.send(f'Играем : {name_current_music} :headphones:')
    except Exception as e:
        await ctx.send("Произошла непредвиденная ошибка, забавно, но я сейчас даже не про тебя :blush:")
        print('Ошибка:\n', traceback.format_exc())


@bot.command()
async def next(ctx):
    """Следующая композиция в плейлисте"""
    try:
        if vc.is_playing() or vc.is_pause():
            vc.stop()
            await play(ctx)
    except:
        await ctx.send("В плейлисте ничего нет :confused:")


@bot.command()
async def pause(ctx):
    """Приостановить или продолжить воспроизведение музыки"""
    if vc.is_playing():
        vc.pause()
        await ctx.send(f'Пауза в твоей счастливой жизни :confused:')
    elif vc.is_paused():
        vc.resume()
        await ctx.send(f'Возращаем радость и страдания :kissing_heart:')

@bot.command()
async def resume(ctx):
    """Продолжить проигрывание музыки"""
    if vc.is_paused():
        vc.resume()
        await ctx.send(f'Возращаем радость и страдания, какой ты умный, знаешь слово "resume" :nerd:')
        
@bot.command()
async def stop(ctx):
    """Остановить проигрывание музыки? Себя останови!"""
    try:
        if vc.is_playing() or vc.is_pause():
            vc.stop()
            await ctx.send(f'Моя остановочка :broken_heart:')
    except:
        print("Останавливать нечего")

@bot.command()
async def delete(ctx, arg):
    """Для удаления песни, надо указать номер песни из playlist"""
    try:
        arg = int(arg) - 1
        play_list.pop(arg)
        name_list.pop(arg)
    except:
        await ctx.send("Не верный номер песни, а может ты просто дурачок :face_with_raised_eyebrow:")


@bot.command()
async def playlist(ctx):
    """Посмотреть плейлист"""
    song_name = ''
    for i in range(len(name_list)):
        song_name += str(i+1) + ' ' + name_list[i] + '\n'
    embed = discord.Embed(color = 0xff9900, title = 'Playlist') # Создание Embed'a
    embed.set_image(url = "https://itc.ua/wp-content/uploads/2019/09/Apple-Music-Android.jpg") # Устанавливаем картинку Embed'a
    embed.add_field(name='Песенки :heart_exclamation:', value=song_name)

    await ctx.send(embed = embed) # Отправляем Embed

@bot.command()
async def петухи(ctx):
    await ctx.send(f'На сервере присутвует только 1 петух **Medvet(Кирилл)#3679** :rooster: ')
    

f_token = open("token.token")
token = f_token.read()
f_token.close()

bot.run(token)
