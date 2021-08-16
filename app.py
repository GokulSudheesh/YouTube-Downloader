from flask import Flask, render_template, request, redirect, url_for, send_file
import thumbnail
from thumbnail import Thumbnail
from youtube import Youtube
import os

app = Flask(__name__)
ytbe = None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/show', methods=['POST'])
def show():
    global ytbe
    try:
        url = request.form['url']
        #print(url)
        ytbe = Youtube(url.strip(" "))
        thumb = Thumbnail(url.strip(" "), ytbe.filename)
        title =  ytbe.title

        # Get the thumbnail of the video
        thumb.get_thumbnail()
        image_path = os.path.join("thumbnails", ytbe.filename+".jpg")
        text = ""
        if (thumbnail.check_rickroll(image_path)>0.60): #RickRollCheck if SSIM is more than 60%
            text = "Its a Rick Roll! Proceed at your own risk."
        result = {
            "image_path" : thumb.image_link,
            "title" : title,
            "text" : text,
            "duration" : ytbe.duration,
            "views" : str(ytbe.views)
        }
        return render_template("show.html", result = result)
    except:
        return render_template("failure.html")

@app.route('/download', methods=['POST'])
def download():
    try:
        format = request.form['format']
        file = None
        if (format == "mp3"):
            ytbe.download_audio()
            file = os.path.join("audio", ytbe.filename+".mp3")
        elif (format == "mp4"):
            ytbe.download_video()
            file = os.path.join("video", ytbe.filename+".mp4")
        return send_file(file, as_attachment=True)
    except:
        return render_template("failure.html")

@app.route('/failure', methods=['POST'])
def gokul():
    return redirect("/") # redirect the user to homepage

if __name__ == '__main__':
    app.run(debug=True)