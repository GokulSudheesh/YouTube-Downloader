import youtube_dl
import os

def meta(url):
    # Returns a dictionary with meta data like title, Views, Likes, Dislikes etc
    ydl_opts = {}
    meta = None
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
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
    return ({"title": meta["title"],
            "filename": format_title(meta["title"]),
             "views": meta["view_count"],
             "duration": meta["duration"]
             })


def format_title(title):
    illegal_chars = ["#", "<", ">", "$", "+", "%", "!", "`", "&", "*", "\'", "\"", "|",
                     "{", "}", "/", "\\", ":", "@"]
    for char in illegal_chars:
        title = title.replace(char, "-")
    return title

def download_video(url, filename):
    ydl_opts = {
        'format': 'best',
        'videoformat': 'mp4',
        'outtmpl' : os.path.join("video", filename+'.mp4')
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return ydl_opts['outtmpl']

def download_audio(url, filename):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl' : os.path.join("audio", filename+'.mp3')
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return ydl_opts['outtmpl']

if __name__ == '__main__':
    url = "https://youtu.be/hM_kejkWeHU"
    url = "https://youtu.be/L_LUpnjgPso"
    url = "https://youtu.be/Dcjk8vF4n38"
    url = "https://www.youtube.com/watch?v=Dcjk8vF4n38"
    url = "https://www.youtube.com/watch?v=TcdEOHV3PgA"