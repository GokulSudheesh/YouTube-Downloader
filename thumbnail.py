import urllib.request
import re
from skimage.metrics import structural_similarity as ssim
import cv2


'''def get_thumbnail(url):
    src = urllib.request.urlopen(url).read()
    info = urllib.parse.parse_qs(src.decode('unicode_escape'))
    #print(info)
    for key, value in info.items():
        #print(key)
        #print(value)
        val = "\"thumbnail\":{\"thumbnails\":[{\"url\":\""
        for v in value:
            ind = v.find(val)
            if ind is not -1:
                print(ind)
                print("Heyy ",v[ind+len(val):ind+len(val)+len(v)])
                break
    print("Done")'''

class Thumbnail:
    def __init__(self, url, title):
        self.url = self.format_url(url)
        self.src = urllib.request.urlopen(self.url).read()
        self.info = urllib.parse.parse_qs(self.src.decode('unicode_escape'))
        self.title = title
        self.image_link = self.get_thumbnail_link()

    def format_url(self, url):
        if "watch?v=" in url:
            #url = "https://youtu.be/"+url.strip("https://www.youtube.com/watch?v=")
            url = "https://youtu.be/"+url.split("watch?v=")[1]
            url = url.split("&")[0]
        return url

    def get_thumbnail(self):        
        if self.image_link != None and self.title != None:
            urllib.request.urlretrieve(self.image_link, "./thumbnails/"+self.title+".jpg")
            if __debug__:                
                print(f"{self.image_link} Image Saved")
        else:
            if __debug__:
                print(f"{self.image_link} Image not Saved")

    def get_thumbnail_link(self):
        #print(self.info)
        for key, value in self.info.items():
            #print(key)
            #print(value)
            regex = "\"thumbnail\":{\"thumbnails\":\[{\"url\":\".*\"width\""

            for v in value:
                match = re.findall(regex,v) # Returns a list of matched strings
                if len(match) != 0:
                    #print(match)
                    return("htt"+match[0].lstrip("[\'\"thumbnail\":{\"thumbnails\":[{\"url\":\"").rstrip("\",\"width\"\']"))
        return None

def check_rickroll(img_path):
    rickrolls = ["rick/rickroll1.jpg", "rick/rickroll2.jpg", "rick/rickroll3.jpg"]
    ssims = []
    for rick in rickrolls:
        im1 = cv2.imread(rick, 0)
        im2 = cv2.imread(img_path, 0)
        im2 = cv2.resize(im2, (im1.shape[1], im1.shape[0])) # Both the images must have same size
        ssims.append(ssim(im1, im2))
    if __debug__:
        print("Rick Rolls: ", ssims)
    return max(ssims)

if __name__ == '__main__':
    url = "https://youtu.be/dQw4w9WgXcQ"
    #url = "https://youtu.be/IYEh0h_mMu8"
    #url = "https://youtu.be/odhMmAPDc54"
    #url = "https://youtu.be/oXRRlBImXT0"
    #url = "https://youtu.be/jNQXAC9IVRw"
    thumb = Thumbnail(url)
    thumb.get_thumbnail()
    print(thumb.title)