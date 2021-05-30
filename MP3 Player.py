#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from mutagen.easyid3 import EasyID3
import pygame
from tkinter.filedialog import *
from tkinter import *

pygame.init()


class FrameApp(Frame):
    def __init__(self,master):
        super(FrameApp, self).__init__(master)

        self.grid()
        self.paused = False
        self.playlist = list()
        self.actual_song = 0

        self.b1 = Button(self, text="PLAY SONG", command=self.play_music,bg='AntiqueWhite1', width=40)
        self.b1.grid(row=2, column=0)

        self.b2 = Button(self, text="PREVIOUS SONG", command=self.previous_song,bg='AntiqueWhite1',
                         width=40)
        self.b2.grid(row=4, column=0)

        self.b3 = Button(self, text="PAUSE/UNPAUSE", command=self.toggle,bg='AntiqueWhite1', width=40)
        self.b3.grid(row=3, column=0)

        self.b4 = Button(self, text="NEXT SONG", command=self.next_song,bg='AntiqueWhite1', width=40)
        self.b4.grid(row=5, column=0)

        self.b5 = Button(self, text="ADD TO PLAYLIST", command=self.add_to_list,bg='AntiqueWhite1',
                         width=40)
        self.b5.grid(row=1, column=0)

        self.label1 = Label(self, fg='Black', font=('Helvetica 12 bold italic',10), bg='ivory2')
        self.label1.grid(row=6, column=0)

        self.output = Text(self, wrap=WORD, width=60)
        self.output.grid(row=8, column=0)

        # set event to not predefined value in pygame
        self.SONG_END = pygame.USEREVENT + 1

        # TODO: Make progressbar, delete songs from playlist, amplify volume

    def add_to_list(self):
        """
        Opens window to browse data on disk and adds selected songs to play list
        :return: None
        """
        directory = askopenfilenames()
        # appends song directory on disk to playlist in memory
        for song_dir in directory:
            print(song_dir)
            self.playlist.append(song_dir)
        self.output.delete(0.0, END)

        for key, item in enumerate(self.playlist):
            # appends song to textbox
            song = EasyID3(item)
            song_data = (str(key + 1) + ' : ' + song['title'][0] + ' - '
                         + song['artist'][0])
            self.output.insert(END, song_data + '\n')

    def song_data(self):
        """
        Makes string of current playing song data over the text box
        :return: string - current song data
        """
        song = EasyID3(self.playlist[self.actual_song])
        song_data = "Now playing: Nr:" + str(self.actual_song + 1) + " " +                     str(song['title']) + " - " + str(song['artist'])
        return song_data

    def play_music(self):
        """
        Loads current song, plays it, sets event on song finish
        :return: None
        """
        directory = self.playlist[self.actual_song]
        pygame.mixer.music.load(directory)
        pygame.mixer.music.play(1, 0.0)
        pygame.mixer.music.set_endevent(self.SONG_END)
        self.paused = False
        self.label1['text'] = self.song_data()

    def check_music(self):
        """
        Listens to END_MUSIC event and triggers next song to play if current 
        song has finished
        :return: None
        """
        for event in pygame.event.get():
            if event.type == self.SONG_END:
                self.next_song()

    def toggle(self):
        """
        Toggles current song
        :return: None
        """
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        elif not self.paused:
            pygame.mixer.music.pause()
            self.paused = True

    def get_next_song(self):
        """
        Gets next song number on playlist
        :return: int - next song number
        """
        if self.actual_song + 2 <= len(self.playlist):
            return self.actual_song + 1
        else:
            return 0

    def next_song(self):
        """
        Plays next song
        :return: None
        """
        self.actual_song = self.get_next_song()
        self.play_music()

    def get_previous_song(self):
        """
        Gets previous song number on playlist and returns it
        :return: int - prevoius song number on playlist
        """
        if self.actual_song - 1 >= 0:
            return self.actual_song - 1
        else:
            return len(self.playlist) - 1

    def previous_song(self):
        """
        Plays prevoius song
        :return: 
        """
        self.actual_song = self.get_previous_song()
        self.play_music()


window = Tk()
window.geometry("500x500")
window.title("MP3 Music Player")



app = FrameApp(window)

while True:
    # runs mainloop of program
    app.check_music()
    app.update()


# In[ ]:




