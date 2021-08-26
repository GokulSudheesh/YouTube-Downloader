from flask import Flask, render_template, request, redirect, url_for, send_file
import thumbnail
from thumbnail import Thumbnail
import youtube as ytbe
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/show', methods=['POST'])
def show():
    try:
        url = request.form['url'].strip(" ")
        #print(url)
        meta = ytbe.meta(url)
        thumb = Thumbnail(url, meta["filename"])

        # Get the thumbnail of the video
        thumb.get_thumbnail()
        image_path = os.path.join("thumbnails", meta["filename"]+".jpg")
        text = ""
        if (thumbnail.check_rickroll(image_path)>0.60): #RickRollCheck if SSIM is more than 60%
            text = "Its a Rick Roll! Proceed at your own risk."
        result = {
            "download": {"url": url, "filename": meta["filename"]},
            "image_path": thumb.image_link,
            "title": meta["title"],
            "text": text,
            "duration": meta["duration"],
            "views": str(meta["views"])
        }
        return render_template("show.html", result = result)
    except Exception as e:
        print(e)
        return render_template("failure.html")

@app.route('/download', methods=['POST'])
def download():
    try:
        format = request.form['format']
        download = eval(request.form['Download'])
        url = download['url']
        filename = download['filename']
        if (format == "mp3"):
            file = ytbe.download_audio(url, filename)
        elif (format == "mp4"):
            file = ytbe.download_video(url, filename)
        return send_file(file, as_attachment=True)
    except Exception as e:
        print(e)
        return render_template("failure.html")

@app.route('/failure', methods=['POST'])
def gokul():
    return redirect("/") # redirect the user to homepage

if __name__ == '__main__':
    app.run(debug=True)