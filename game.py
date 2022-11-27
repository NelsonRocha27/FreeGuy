import os

import requests


class Game:
    name = None
    link = None
    platform = None
    image = None
    provider = None
    status = None
    date = None
    imageLocalPath = None

    def __init__(self):
        self.name = None
        self.link = None
        self.platform = None
        self.image = None
        self.provider = None
        self.status = None
        self.date = None
        self.imageLocalPath = os.path.dirname(os.path.abspath(__file__)) + "\\prime_gaming_image.jpg"

    def AddName(self, name):
        self.name = name

    def GetName(self):
        return self.name

    def AddLink(self, link):
        self.link = link

    def GetLink(self):
        return self.link

    def AddPlatform(self, platform):
        self.platform = platform

    def GetPlatform(self):
        return self.platform

    def AddImage(self, image):
        self.image = image

    def GetImage(self):
        return self.image

    def AddProvider(self, provider):
        self.provider = provider

    def GetProvider(self):
        return self.provider

    def AddStatus(self, status):
        self.status = status

    def GetStatus(self):
        return self.status

    def AddDate(self, date):
        self.date = date

    def GetDate(self):
        return self.date

    def IsFreeToKeep(self, free_with_prime):
        if self.status.lower() == "free to keep":
            return True
        elif free_with_prime is True and self.status.lower() == "free with prime":
            return True
        else:
            return False

    def IsPCGame(self):
        if self.platform.lower() == "pc":
            return True
        else:
            return False

    def IsRepeated(self, list_of_games):
        for game in list_of_games:
            if self.name == game.name and self.provider == game.provider and self.platform == game.platform and self.link == game.link:
                return True

        return False

    def Message(self):
        return "[" + self.provider.upper() + "] - " + self.name + "\n" + self.link + "\n"

    def DownloadImageFromURL(self):
        img_data = requests.get(self.image).content
        with open(self.imageLocalPath, 'wb') as handler:
            handler.write(img_data)

    def DeleteImageDownload(self):
        if os.path.exists(self.imageLocalPath):
            os.remove(self.imageLocalPath)
        else:
            print("The image does not exist")
