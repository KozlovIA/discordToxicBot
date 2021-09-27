# This Python file uses the following encoding: utf-8
from os import read
import sys, time
import numpy as np
from PyQt6 import QtGui, uic, QtWidgets, QtCore
from PySide6 import QtWidgets
import functional
import requests
from bs4 import BeautifulSoup
import threading

ToxicFunctional = functional.PlayMusic()

class PlayMusic():
    def __init__(self) -> None:
        self.songName = ""

    def input_song_name(self, songName):
        return self.songName


    def searchUrl_and_add_to_playlist(self):        # поиск ссылки по названию и записывание в плейлист 
        music_name = self.songName
        if True:
            video = True
        else:
            video = False
        if len(music_name) > 5:
            if music_name[0]+music_name[1]+music_name[2]+music_name[3]+music_name[4]+music_name[5] == "https:":
                clip = requests.get(music_name)     # частично копия из searchUrl, для вывода названия песни
                inspect = BeautifulSoup(clip.content, "html.parser")
                yt_title = inspect.find_all("meta", property="og:title")
                for concatMusic1 in yt_title:
                    pass
                ToxicFunctional.addNext(music_name, concatMusic1['content'], video)
            else:
                [url, name] = ToxicFunctional.searchUrl(music_name=music_name)
                ToxicFunctional.addNext(url, name, video)
        else:
            if len(music_name) > 1:
                [url, name] = ToxicFunctional.searchUrl(music_name=music_name)
                ToxicFunctional.addNext(url, name, video)
        self.out_play_list()

    def play_pause(self):       # начать воспроизведение
        if ToxicFunctional.firstPlay:
            ToxicFunctional.currentTime = 0
            ToxicFunctional.play()
            ToxicFunctional.firstPlay = False
        else:
            ToxicFunctional.player.pause()
        time.sleep(0.5)
        if ToxicFunctional.player.is_playing() == 1:
            self.set_time_for_ui()
            self.set_time_song_for_ui()

    def playNext(self):     # воспроизвести следующую
        if ToxicFunctional.numberSongName_Play < ToxicFunctional.numberSong:
            ToxicFunctional.playNext()
            time.sleep(0.5)
            self.set_time_song_for_ui()
            self.set_time_for_ui()
            self.out_play_list()
    def playPrevious(self):     # воспроизвести предыдущую
        if ToxicFunctional.numberSongName_Play > 0:
            ToxicFunctional.playPrevious()
            time.sleep(0.5)
            self.set_time_song_for_ui()
            self.set_time_for_ui()
            self.out_play_list()

    def stop():     # остановка воспроизведения
        ToxicFunctional.stop()
        ToxicFunctional.firstPlay = True

    def set_time_song_for_ui():     # set time song in ui
        songTime = ToxicFunctional.get_length()
        minutes = int(songTime/(1000*60))
        seconds = str((songTime/(1000*60) - minutes) / 10 * 6)
        seconds = seconds[2] + seconds[3]

    def set_time_for_ui(self, Timer = True):      # вывод времени от начала песни
        currentTime=0
        if ToxicFunctional.videoCheck[ToxicFunctional.numberSongName_Play] == True:     # Вывод в случае видео, всё работает
            currentTime = ToxicFunctional.get_time()
        else:
            currentTime = int((time.monotonic_ns() - ToxicFunctional.startSongTime)/10**6) + ToxicFunctional.timeAdd
            ToxicFunctional.currentTime = currentTime
        minutes = int(currentTime/(1000*60))
        seconds = str((currentTime/(1000*60) - minutes) / 10 * 6)
        if len(str(currentTime)) > 3:
            seconds = seconds[2] + seconds[3]
        thread = threading.Timer(1, self.set_time_for_ui)
        thread.start()
        if ToxicFunctional.player.is_playing() == 0 or Timer == False:
            thread.cancel()
        if currentTime >= ToxicFunctional.get_length():
            time.sleep(0.4)
            self.playNext()

    def stop_time_ui(self):     # остановка таймера для функции установки времени
        self.set_time_for_ui(Timer=False)

    def out_play_list():    # вывод названий песен в лист
            for i in range(ToxicFunctional.numberSong):
                songName = ToxicFunctional.songName[i]
                #ui.playlistWidget.setStyleSheet
                #print(colored())
                #ui.playlistWidget.addItem('{}. {}'.format(i+1, songName))
#---------------------------------------------------------------------------------------------------------