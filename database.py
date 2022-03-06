from datetime import datetime, timedelta

from pymongo import MongoClient


class DataBase:
    gamesDBID = "GamesDB"
    cluster = None
    db = None
    collection = None
    listOfTeams = []
    newGame = False

    def __init__(self, url):
        self.cluster = MongoClient(url)
        self.db = self.cluster["FreeGuyDB"]
        self.collection = self.db["Games"]
        self.newGame = False

    def Add_Game(self, game):
        self.newGame = False
        gamesDBIDQuery = {"_id": self.gamesDBID}
        gameQuery = {"name": game.name, "link": game.link, "platform": game.platform, "image": game.image,
                     "provider": game.provider, "status": game.status, "date": game.date}

        if self.collection.count_documents(gamesDBIDQuery) == 0:
            post = {"_id": self.gamesDBID, "game": [gameQuery]}
            self.collection.insert_one(post)
            self.newGame = True
        else:
            if self.Is_Game_Advertiseable(game, 30):
                self.collection.update_one({"_id": self.gamesDBID}, {"$push": {"game": gameQuery}})
                self.newGame = True

    """
    Check if game exists in database already. If the game exists and was placed in database in a space time 
    shorter than 'timeframe' (in days) returns false, otherwise returns true     
    """

    def Is_Game_Advertiseable(self, game, timeframe):
        listOfGames = []
        for document in self.collection.find({"_id": self.gamesDBID, "game": {"$exists": True}}):
            listOfGames = document['game']

        for dbGame in listOfGames:
            dbGameDateTimeObj = datetime.strptime(game.date, "%d/%m/%Y")
            timeElapsed = datetime.today() - dbGameDateTimeObj
            nrDays = timedelta(days=timeframe)
            if dbGame.get('name') == game.name and dbGame.get('provider') == game.provider \
                    and dbGame.get('platform') == game.platform and dbGame.get('link') == game.link \
                    and timeElapsed < nrDays:
                return False
        return True

    def Define_Text_Channel(self, guild_id, channel_id):
        if self.collection.count_documents({"_id": guild_id}) == 0:
            self.collection.insert_one({"_id": guild_id, "textChannelID": channel_id})
        else:
            self.collection.update_one({"_id": guild_id}, {"$set": {"textChannelID": channel_id}})

    def Get_Text_Channel(self, guild_id):
        id = None
        for document in self.collection.find({"_id": guild_id, "textChannelID": {"$exists": True}}):
            id = document['textChannelID']

        if id is None:
            return None
        else:
            return id

    def Is_New_Game(self):
        if self.newGame:
            return True
        else:
            return False

    """def List_Teams(self, guild_id):
        for document in self.collection.find({"_id": guild_id, "team": {"$exists": True}}):
            self.listOfTeams = document['team']

        if len(self.listOfTeams) > 0:
            return True
        else:
            return False"""

    """def Define_Text_Channel(self, guild_id, channel_id):
        self.collection.update_one({"_id": guild_id}, {"$set": {"textChannelID": channel_id}})

    def Get_Text_Channel(self, guild_id):
        id = None
        for document in self.collection.find({"_id": guild_id, "textChannelID": {"$exists": True}}):
            id = document['textChannelID']

        if id is None:
            return None
        else:
            return id

    def Get_List_Teams_As_String(self, guild_id):
        if self.List_Teams(guild_id):
            return '\n'.join(self.listOfTeams)

    def Get_List_Teams(self, guild_id):
        if self.List_Teams(guild_id):
            return self.listOfTeams"""
