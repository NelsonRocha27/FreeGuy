import os
from database import DataBase
from dotenv import load_dotenv
from discord.ext import commands
from webscrapper import WebScrape

load_dotenv()

client = commands.Bot(command_prefix='.')
db = DataBase(os.getenv('DBURL'))
guilds = {}


@client.event
async def on_ready():
    text_channel = None

    for guild in client.guilds:
        text_channel_id = db.Get_Text_Channel(guild.id)
        if text_channel_id is not None:
            text_channel = text_channel_id
        else:
            text_channel_list = []
            for channel in guild.text_channels:
                text_channel_list.append(channel.id)
            text_channel = text_channel_list[0]
        guilds[guild.id] = text_channel

    print('Bot is now logged in as {0.user}'.format(client))
    WebScrape()
    list = WebScrape.games_list
    for game in list:
        db.Add_Game(game)


@client.command()
async def ping(ctx):
    await ctx.send('pong')


@client.command(aliases=['here'])
async def set_text_channel(ctx):
    for guild in guilds:
        if guild == ctx.guild.id:
            guilds[guild] = ctx.channel.id
    db.Define_Text_Channel(ctx.guild.id, ctx.channel.id)


client.run(os.getenv('TOKEN'))
pass
