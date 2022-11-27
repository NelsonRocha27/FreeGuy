import asyncio
import os
import discord
from database import DataBase
from dotenv import load_dotenv
from discord.ext import commands
from webscrapper import WebScrape

load_dotenv()

client = commands.Bot(command_prefix='*')
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
    client.loop.create_task(Listen_For_New_Games())


@client.command(aliases=['echo'])
async def Echo_Game(ctx, link):
    await ctx.send(link + "\n")


@client.command(aliases=['here'])
async def set_text_channel(ctx):
    for guild in guilds:
        if guild == ctx.guild.id:
            guilds[guild] = ctx.channel.id
    db.Define_Text_Channel(ctx.guild.id, ctx.channel.id)


async def Listen_For_New_Games():
    await client.wait_until_ready()
    message_link = None

    while not client.is_closed():

        WebScrape()
        list = WebScrape.games_list
        for game in list:
            db.Add_Game(game)
            if db.Is_New_Game():
                for guild in guilds:
                    if guilds[guild] is not None:
                        channel = client.get_channel(guilds[guild])
                    else:
                        text_channel_list = []
                        for channel in guild.text_channels:
                            text_channel_list.append(channel)
                        channel = text_channel_list[0]
                    if game.provider == "prime gaming":
                        game.DownloadImageFromURL()
                        file = discord.File(game.imageLocalPath, filename=game.imageLocalPath)
                        await channel.send(game.Message(), file=file)
                        game.DeleteImageDownload()
                    else:
                        await channel.send(game.Message())

        await asyncio.sleep(3600)  # task runs every 1 hour

client.run(os.getenv('TOKEN'))
pass
