import requests
import json
import re
import os

class Ins:
    def __init__(self):
        self.user = "user"
        self.oldTypeAndCodes = []

    def getTypeAndCodes(self):
        homeURL = "https://www.instagram.com/" + self.user + "/"
        homeHtml = requests.get(homeURL).text
        # print(homeHtml)

        m = re.search('"edge_owner_to_timeline_media".*?,"edge_saved_media"', homeHtml)
        usefulData = m.string[m.start() + 31 : m.end() - 19]
        # print(usefulData)

        data = json.loads(usefulData)["edges"]

        typeAndCode = []
        for i in data:
            # print(i)
            dict = {}
            dict["type"] = i["node"]["__typename"]
            dict["code"] = i["node"]["shortcode"]
            typeAndCode.append(dict)

        self.oldTypeAndCodes = typeAndCode
        return typeAndCode

    def getGraphImageURL(self, code):
        pageURL = "https://www.instagram.com/p/" + code + "/?taken-by=" + self.user
        pageHTML = requests.get(pageURL).text
        # print(pageHTML)

        m = re.search('"display_url":.*?,"display_resources"', pageHTML)
        imageURL = m.string[m.start() + 15 : m.end() - 21]
        # print(imageURL)
        return imageURL

    def getGraphSidecarURLs(self, code):
        pageURL = "https://www.instagram.com/p/" + code + "/?taken-by=" + self.user
        pageHtml = requests.get(pageURL).text
        # print(pageHtml)

        m = re.search('"edge_sidecar_to_children".*?}}}]},"gatekeepers"', pageHtml)
        usefulData = m.string[m.start() + 27 : m.end() - 19]
        dictList = json.loads(usefulData)["edges"]

        imgURLs = []
        for dict in dictList:
            imgURLs.append(dict["node"]["display_url"])

        return imgURLs

    def getGraphVideoURL(self, code):
        pageURL = "https://www.instagram.com/p/" + code + "/?taken-by=" + self.user
        pageHTML = requests.get(pageURL).text
        # print(pageHTML)

        m = re.search('"video_url":.*?,"video_view_count"', pageHTML)
        videoURL = m.string[m.start() + 13 : m.end() - 20]

        m = re.search('"display_url":.*?,"display_resources"', pageHTML)
        imageURL = m.string[m.start() + 15: m.end() - 21]

        result = {}
        result["videoURL"] = videoURL
        result["imageURL"] = imageURL

        return result

    def getText(self, code):
        pageURL = "https://www.instagram.com/p/" + code + "/?taken-by=" + self.user
        pageHTML = requests.get(pageURL).text

        m = re.search('on Instagram:.*?\n', pageHTML)
        text = m.string[m.start() + 15 : m.end() - 2]
        return text

    def checkUpdate(self):
        updates = 0
        newTypeAndCodes = []

        if len(self.oldTypeAndCodes) == 0:
            self.getTypeAndCodes()
        else:
            oldFirst = self.oldTypeAndCodes[0]
            newTypeAndCodes = self.getTypeAndCodes()

            for newItem in newTypeAndCodes:
                if newItem == oldFirst:
                    break
                else:
                    updates += 1

        if updates != 0:
            updateTypeAndCodes = newTypeAndCodes[0 : updates]
            self.getUpdates(updateTypeAndCodes)

    def getUpdates(self, updateTypeAndCodes): # private, called by checkUpdate()
        updateTypeAndCodes.reverse()

        i = 1
        for typeAndCode in updateTypeAndCodes:

            if typeAndCode["type"] == "GraphImage":
                path = "./" + str(i) + "_singalImage" + "/"
                os.makedirs(path)

                text = self.getText(typeAndCode["code"])
                with open(path + "txt", "w") as txt:
                    txt.write(text)

                imgURL = self.getGraphImageURL(typeAndCode["code"])
                r = requests.get(imgURL, stream=True)
                with open(path + "img", 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

            elif typeAndCode["type"] == "GraphVideo":
                path = "./" + str(i) + "_video" + "/"
                os.makedirs(path)

                text = self.getText(typeAndCode["code"])
                with open(path + "txt", "w") as txt:
                    txt.write(text)

                # videoURL = self.getGraphVideoURL(typeAndCode["code"])["videoURL"]
                # r = requests.get(videoURL, stream=True)
                # with open(path + "video", 'wb') as f:
                #     for chunk in r:
                #         f.write(chunk)

                imgURL = self.getGraphVideoURL(typeAndCode["code"])["imageURL"]
                r = requests.get(imgURL, stream=True)
                with open(path + "img", 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

            else: # GraphSidecar
                path = "./" + str(i) + "_multiImages" + "/"
                os.makedirs(path)

                text = self.getText(typeAndCode["code"])
                with open(path + "txt", "w") as txt:
                    txt.write(text)

                imgURLs = self.getGraphSidecarURLs(typeAndCode["code"])
                j = 1

                for url in imgURLs:
                    r = requests.get(url, stream=True)
                    with open(path + "img" + str(j), 'wb') as f:
                        for chunk in r:
                            f.write(chunk)
                    j += 1

            i += 1


