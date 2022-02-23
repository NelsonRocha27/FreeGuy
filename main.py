import os
from database import DataBase
from dotenv import load_dotenv
from discord.ext import commands
from webscrapper import WebScrape

load_dotenv()

client = commands.Bot(command_prefix='.')
db = DataBase(os.getenv('DBURL'))


@client.event
async def on_ready():
    print('Bot is now logged in as {0.user}'.format(client))
    WebScrape()


@client.command()
async def ping(ctx):
    await ctx.send('pong')


@client.command(aliases=['here'])
async def set_text_channel(ctx):
    db.Define_Text_Channel(ctx.guild.id, ctx.channel.id)


client.run(os.getenv('TOKEN'))
pass
