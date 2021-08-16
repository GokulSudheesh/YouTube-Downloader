import os
folders = ["audio", "video", "thumbnails"]

for folder in folders:
    for file in os.listdir(folder):
        os.remove(os.path.join(folder, file))