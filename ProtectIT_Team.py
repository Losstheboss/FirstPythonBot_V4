import discord
import json
import datetime
import pytz
import asyncio
from discord.ext import commands

...

# other imports you need

# make a class with your name as a commands.Cog class.
class ProtectITM(commands.Cog):
    # as this is not the main file you need to make a global variable called bot.
    def __init__(self, bot):
        self.bot = bot
        # define other variables

        ### Prepare the Blocked_Words List ##


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            Original = before.display_name
            NewName = after.display_name

            ActualUN = before
            userName = None
            print(str(ActualUN))


            utc_now = pytz.utc.localize(datetime.datetime.utcnow())
            pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
            timenow = pst_now.strftime("%H:%M:%S")

            print(userName)

            listofnames = ["Tom Bilyeu", "Lisa Bilyeu", "Will Vu", "Chase Caprio", "Namrata Doshi", "Amy McCarthy",
                           "Jeremy Mary", "Kevin Loss", "Impact Theory"]

            for name in listofnames:
                print("1.Name being checked: " + name)
                print("2.Before Name: " + str(Original))
                print("3.After Name: " + str(NewName))
                if NewName.lower() == name.lower():
                    print(" --Match Confirmed --")
                    print(f"Original name: {Original} : New Nick: {NewName} ")
                    DMmsg = ("There can only be one " + name + ". Unfortunately, you are not it. "
                                                               "Your nickname has reverted.")
                    await after.edit(nick=None)
                    await ActualUN.send(DMmsg)
                    print("Message Sent.")
                    try:
                        with open("Logs/ProtectLog.txt", "a") as f:
                            f.write(
                                f"Date: {timenow}, Username: {Original}, Attempted username: {name}, Message: {DMmsg}\n")
                            await asyncio.sleep(2)
                    except Exception as e:
                        print(e)
                        await asyncio.sleep(2)


def setup(bot):
    bot.add_cog(ProtectITM(bot))