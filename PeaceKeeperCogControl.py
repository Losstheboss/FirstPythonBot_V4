import discord
from discord.ext.commands import Bot
import json
import datetime
import pytz
import asyncio


#Bot Login Steps

def read_token():
    with open("Config/T_Peacekeeper.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

client = Bot('!')

global pathwaytocog

pathwaytocog ="cogs"

initial_cogs = [
    'cogs.Logger',
    'cogs.OnJoinSetup',
    'cogs.PeaceKeeper_v4',
    'cogs.ProtectIT_Team'
]

print('Connecting...')

@client.event
async def on_ready():
    # client.load_extension("/Users/Dazin/PycharmProjects/ITLDiscordBot/cogs/Logger.py")
    # client.load_extension("/Users/Dazin/PycharmProjects/ITLDiscordBot/cogs/PeaceKeeper.py")
    # client.load_extension("/Users/Dazin/PycharmProjects/ITLDiscordBot/cogs/ProtectIT_Team.py")
    # client.load_extension("/Users/Dazin/PycharmProjects/ITLDiscordBot/cogs/OnJoinSetup.py")

    for ext in initial_cogs:
        client.load_extension(ext)
   # print(f'Loaded all extensions after {human_timedelta(self.start_time, brief=True, suffix=False)}')
        print("Loaded Extension: " + str(ext))


@client.command
async def Coglist(ctx):
    embed = discord.Embed(title="Cog List", description="For now")
    embed.add_field(name="Logger:", value="Merp")
    embed.add_field(name="OnJoinSetup:", value="Merp")
    embed.add_field(name="PeaceKeeper:", value="Merp")
    embed.add_field(name="ProtectIT_Team:", value="Merp")

    await ctx.channel.send(content=None, embed=embed)

async def LoadUp(Cog: str):
    client.load_extension(pathwaytocog + Cog)
   # await client.channel.send("Roger that, " + str(Cog) + "Cog Loaded!")

async def UnLoadIt(Cog: str):
    client.unload_extension(pathwaytocog + Cog)
   # await client.channel.send("Roger that, " + str(Cog) + "Cog Unloaded!")

async def ReloadIt(Cog: str):
    # await client.channel.send("Roger that, " + str(Cog) + "Cog Unloading!")
    client.unload_extension(pathwaytocog + Cog)
    # await client.channel.send("Roger that, " + str(Cog) + "Cog Unloaded!")
    client.unload_extension(pathwaytocog + Cog)
    # await client.channel.send("Roger that, " + str(Cog) + "Cog Reloaded!")


client.run(token)