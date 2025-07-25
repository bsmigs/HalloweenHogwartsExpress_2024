import os
import vlc
import numpy as np
import time
import threading

class Train:
    
    def __init__(self, label):
        mypath = "/home/pi/repos/HalloweenHogwartsExpress_2024/"
        self.label = label
        self.song_playing = False
        if (label == "music"):
            self.path = mypath+"music"
        elif (label == "horn"):
            self.path = mypath+"horn_sounds_mp3s"
        elif (label == "wheels"):
            self.path = mypath+"wheel_sounds_mp3s"
        elif (label == "engine"):
            self.path = mypath+"engine_sounds_mp3s"

        self.music_list = os.listdir(self.path)
        print(f"there are {len(self.music_list)} sounds or music")

        # set sounds/music counter = 0 initially
        self.counter = 0

        # track release status since trying to release more
        # than once can cause issues
        self.is_released = False

        # track if we will be looping through songs
        self.is_looping = False

        # track the volume since every time
        # self.media is released the volume is set equal
        # to 0 again
        self.curr_volume = 70

        self.media = vlc.MediaPlayer()

    def play_song(self):
        if (self.media.is_playing()):
            # don't want to do anything if something already playing
            return
        else:
            self.media = vlc.MediaPlayer(self.path+"/"+self.music_list[self.counter])
            self.media.play()
            print(f"Current volume = {self.curr_volume}")
            self.media.audio_set_volume(self.curr_volume)
            self.is_released = False

    def is_playing(self):
        return self.media.is_playing()

    def change_looping_status(self):
        self.is_looping = not self.is_looping
        print(f"Looping status now set to {self.is_looping}")

    def release(self):
        if (not self.is_released):
            self.media.release()
            self.is_released = True

    def did_song_end(self):
        if (self.media.get_state() == vlc.State.Ended):
            return True
        else:
            return False

    def check_playback_status(self):
        while True:
            if not self.is_playing():
                print(f"State = {self.media.get_state()}")
                if self.media.get_state() == vlc.State.Ended:
                    print(f"Song finished playing")
                    self.release()
                    break
            time.sleep(0.5)

    def change_counter(self, inc_or_dec):
        if (inc_or_dec == "inc"):
            # increase counter
            self.counter += 1
        elif (inc_or_dec == "dec"):
            # decrease counter
            self.counter -= 1

        if (self.counter >= len(self.music_list) or self.counter < 0):
            self.counter = np.mod(self.counter, len(self.music_list))

    def pause_song(self):
        # any non-zero value pauses it
        self.media.set_pause(1)
        
    def resume_song(self):
        # an argument of 0 makes it resume
        self.media.set_pause(0)
        
    def stop_song(self):
        if (self.media.get_state() == vlc.State.Ended):
            # if song has ended and I try to call
            # self.media.stop(), I'll get a seg fault
            self.release()
        else:
            self.media.stop()
            self.release()
        
    def next_song(self):
        if (self.media.get_state() != vlc.State.Stopped):
            self.stop_song()
        self.change_counter("inc")
        print(f"counter={self.counter}")
        self.play_song()
        
    def previous_song(self):
        if (self.media.get_state() != vlc.State.Stopped):
            self.stop_song()
        self.change_counter("dec")
        print(f"counter={self.counter}")
        self.play_song()

    def set_volume(self, volume):
        if (volume < 0 or volume > 100):
            return
        else:
            self.curr_volume = volume
            self.media.audio_set_volume(volume)

    def get_volume(self):
        return self.curr_volume
       
    
        
        
