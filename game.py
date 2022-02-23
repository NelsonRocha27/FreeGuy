class Game:
    name = None
    link = None
    platform = None
    image = None
    provider = None
    status = None

    def __init__(self):
        self.name = None
        self.link = None
        self.platform = None
        self.image = None
        self.provider = None
        self.status = None

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

    def IsFreeToKeep(self):
        if self.status.lower() == "free to keep":
            return True
        else:
            return False

    def IsRepeated(self, list_of_games):
        for game in list_of_games:
            if self.name == game.name and self.provider == game.provider and self.platform == game.platform and self.link == game.link:
                return True

        return False
