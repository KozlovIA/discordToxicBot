import discord
from discord import client
from playsound import playsound
from pygame import mixer
import pygame
import PyQt6
import source.functional
import source.main

class BotClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))


""" pygame.mixer.init()
pygame.mixer.music.load("LifeEternal.mp3")
pygame.mixer.music.play() """

client = BotClient()
client.run('ODY1Njg3NzM5Mjg1NzY2MjA1.YPHoiA.12p6ZeeWhQh15GxaSEVb1uvaEfg')
