import discord
import json
import datetime
import pytz
import asyncio
from discord.ext import commands

...


# other imports you need

# make a class with your name as a commands.Cog class.
class LoggingCog(commands.Cog):
    # as this is not the main file you need to make a global variable called bot.
    def __init__(self, bot):
        self.bot = bot
        # define other variables


    # add an event using commands.Cog.listener() (not bot.event)
    @commands.Cog.listener()
    async def on_message(self, ctx):
        ### Setup Logger Time
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
        timenow = pst_now.strftime("%H:%M:%S")

        ### Set up Log

        msginlog = ctx.content

        msginlog.strip()
        msginlog = ' '.join(msginlog.split())


        if ctx.author.bot:
            try:
                with open("Logs/Botlog.txt", "a") as f:
                    f.write(
                        f"Channel: {ctx.channel}, Date: {timenow}, Author: {ctx.author}, Message: {msginlog}\n")
                    await asyncio.sleep(2)
            except Exception as e:
                print(e)
                await asyncio.sleep(2)
        else:
            try:
                with open("Logs/Messagelog.txt", "a") as f:
                    f.write(f"Date: {timenow}, Channel: {ctx.channel} Author: {ctx.author}, Message: {msginlog}\n")
                    await asyncio.sleep(2)
            except Exception as e:
                print(e)
                await asyncio.sleep(2)




def setup(bot):
    bot.add_cog(LoggingCog(bot))