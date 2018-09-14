import requests
import os
import time
import shutil


class Weibo:
    def __init__(self):
        self.endfix = "\n------------\nhttp://www.bing.com"
        self.sendURL = "https://api.weibo.com/2/statuses/share.json"
        self.accessToken = "2.00GkKB_H05fZMDc619553530rspZyC"

    def sendSingalImg(self, dirName):
        path = "./" + dirName + "/"
        with open(path + "txt", "r", encoding="utf-8") as textFile:
            text = textFile.read().replace("#", ">") + self.endfix

        image = open(path + "img", "rb")

        r = requests.post(self.sendURL, data = {"access_token": self.accessToken, "status": text},
                          files= {"pic": image})
        image.close()

    def sendMultiImgs(self, dirName):
        path = "./" + dirName + "/"
        with open(path + "txt", "r", encoding="utf-8") as textFile:
            text = textFile.read().replace("#", ">") + self.endfix

        numOfImgs = len(os.listdir(path)) - 1

        for i in range(numOfImgs):
            fileName = "img" + str(numOfImgs - i)
            fraction = "( " + str(numOfImgs - i) + " / " + str(numOfImgs) + " )\n------------\n"

            image = open(path + fileName, "rb")
            r = requests.post(self.sendURL, data={"access_token": self.accessToken, "status": fraction + text},
                              files={"pic": image})
            image.close()
            time.sleep(30)

    def sendVideo(self, dirName):
        path = "./" + dirName + "/"
        with open(path + "txt", "r", encoding="utf-8") as textFile:
            text = textFile.read().replace("#", ">") + self.endfix

        text = "( 原 po 为视频 )\n------------\n" + text

        image = open(path + "img", "rb")
        r = requests.post(self.sendURL, data={"access_token": self.accessToken, "status": text},
                          files={"pic": image})
        image.close()

    def checkNewDirs(self):
        dirs = os.listdir()
        if len(dirs) > 7:
            for dir in dirs:
                if (dir == "ins.py") | (dir == "weibo.py") | (dir == "main.py") | (dir == "__init__.py") | (dir == "nohup.out") | (dir == "__pycache__") | (dir == ".git"):
                    continue

                if "_singalImage" in dir:
                    self.sendSingalImg(dir)
                elif "_video" in dir:
                    self.sendVideo(dir)
                elif "_multiImages" in dir:
                    self.sendMultiImgs(dir)

                shutil.rmtree("./" + dir)

