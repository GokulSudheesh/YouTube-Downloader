import youtube_dl
import os
from tkinter import filedialog
from mttkinter import *

class Youtube:
    def __init__(self, url):
        self.url = url
        self.meta = self.meta()
        self.title = self.meta["title"]
        self.filename = self.format_title(self.meta["title"])
        self.views = self.meta["view_count"]
        self.duration = self.meta["duration"]

    def meta(self):
        # Returns a dictionary with meta data like title, Views, Likes, Dislikes etc
        ydl_opts = {}
        meta = None
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(self.url, download=False)
            if (meta["duration"] < 60 * 60):
                meta["duration"] = "{}:{:02d}".format(int(meta["duration"] / 60), int(meta["duration"]) % 60)
            else:
                meta["duration"] = "{}:{:02d}:{:02d}".format(int(meta["duration"] / 60 / 60),
                                                            int(int(meta["duration"]) % (60 * 60) / 60),
                                                            int(meta["duration"]) % (60 * 60) % 60)
            if __debug__:
                
                #print(meta)
                print("Title: ", meta["title"])
                print("Views: ", meta["view_count"])
                print("Likes: ", meta["like_count"])
                print("Dislikes: ", meta["dislike_count"])
                print("Duration: ", meta["duration"])
        return meta

    def format_title(self, title):
        illegal_chars = ["#", "<", ">", "$", "+", "%", "!", "`", "&", "*", "\'", "\"", "|",
                         "{", "}", "/", "\\", ":", "@"]
        for char in illegal_chars:
            title = title.replace(char, "-")
        return title

    def download_video(self):
        ydl_opts = {
            'format': 'best',
            'videoformat': 'mp4',
            'outtmpl' : os.path.join("video", self.filename+'.mp4')
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    def download_audio(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl' : os.path.join("audio", self.filename+'.mp3')
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

if __name__ == '__main__':
    url = "https://youtu.be/hM_kejkWeHU"
    url = "https://youtu.be/L_LUpnjgPso"
    url = "https://youtu.be/Dcjk8vF4n38"
    url = "https://www.youtube.com/watch?v=Dcjk8vF4n38"
    url = "https://www.youtube.com/watch?v=TcdEOHV3PgA" # Dil se re
    ytbe = Youtube(url)
    root = mtTkinter.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Choose your folder")
    root.destroy()
    ytbe.download_audio(directory)