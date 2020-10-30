import discord
import json
import datetime
import os
import pytz
import time
import asyncio
from discord.ext import commands

with open('Jsons/Blocked_Words.json') as f:
    config = json.load(f)


# other imports you need

# make a class with your name as a commands.Cog class.
class PeaceKeeperCog(commands.Cog):
    cussCounter = {}
#    actionLog

    # as this is not the main file you need to make a global variable called bot.
    def __init__(self, bot):
        self.bot = bot
        # define other variables

        # Possible way to open one time and never close (should work, and might better for async writing)
        # Concern is, if it dies, does it corrupt the file because it never closed it
       # self.actionLog = open("log/ActionLog.txt", "a+")

        ### Prepare the Blocked_Words List ##

    # def writeToActionLog(self, text):
    #     # One way to do it
    #     f = open("log/ActionLog.txt", "a+")
    #     f.write(text)
    #
    #     # OR do it this way if you want ot use the class variable
    #    # self.actionLog.write(text)

    @commands.Cog.listener()
    async def on_message(self, ctx):

        ## Role Exclusions to general text

        # AdminRole = ctx.guild.get_role(role_id=651460197427970078)
        # ModRole = ctx.guild.get_role(role_id=651460101512888331)

        # Prepare to Mute or Give access to user:
        MutedRole = discord.utils.get(ctx.guild.roles, name="MutedRole")

        StandardRole = discord.utils.get(ctx.guild.roles, name="Impactivists")

        ModRole = discord.utils.get(ctx.guild.roles, name="Moderator")

        AdminRole = discord.utils.get(ctx.guild.roles, name="Administrator")

        # Sets basic level
        if ctx.author.bot:
            print("User is a Bot. Nothing else was done.")
        else:
            if ModRole in ctx.author.roles or AdminRole in ctx.author.roles:
                incharge = True
                print("User is a Mod or Admin.")
            else:
                incharge = False
                print("User is not a Mod or Admin.")
            # if AdminRole in ctx.author.roles or ModRole in ctx.author.roles:
            #     Incharge = True


            if any([str.lower(word) in str.lower(ctx.content) for word in config['words']]):
                badword = True
                print("Badword = True")
            else:
                badword = False
                print("Badword = False")

            spmDMwarn = """Automated Warning: It looks like you've said the same thing three times. This is considered spam. If you continue, you will be muted for 24 hours. Please review #impact-theory-guidelines for the server guidelines regarding spam and #positivevibesonly."""

            spmDMmessage = """You have been automatically muted for 24 hours. Please review #impact-theory-guidelines for the server guidelines."""

            blockedDMwarn = """Automated Warning: Please remember the #positivevibesonly guideline when speaking in our server. If you continue, you will be muted for 24 hours. Please review #impact-theory-guidelines for the server guidelines regarding spam and #positivevibesonly."""

            blockedDMmessage = """You have been automatically muted for 24 hours for using vulgar language and/or insulting language. Please review #impact-theory-guidelines for the server guidelines."""

            bothDMwarn = """Automated Warning: Please remember the #positivevibesonly and spamming guidelines when speaking in our server. If you continue, you will be muted for 24 hours. Please review #impact-theory-guidelines for the server guidelines regarding spam and #positivevibesonly."""

            bothDMmessage = """You have been automatically muted for 24 hours for spamming and using vulgar language and/or insulting language. Please review #impact-theory-guidelines for the server guidelines."""

            spmcount = 0
            # userName = ctx.author

            SpmThreetimes = False
            SpmFiveTimes = False
            blkThreetimes = False
            blkFiveTimes = False

            # Spam Check
            async for msg in ctx.channel.history(limit=50):
                if msg.author.id == ctx.author.id and str.lower(ctx.content) == str.lower(
                        msg.content) and ctx.author != ctx.author.bot:
                    spmcount = spmcount + 1

            print("Spmcount: " + str(spmcount))

            #
            # """
            # cussCounter data format (pythin dict)
            # {
            #     "losstheboss":  {
            #         "cussCount" : 0,
            #         "lastCuss" : 234234.33,
            #     },
            #     "asperon": {
            #         "cussCount" : 0,
            #         "lastCuss" : 2342342.34
            #     }
            # }
            # """

    # Sets Counter to 0.
            if ctx.author not in self.cussCounter:
             self.cussCounter[ctx.author] = {'cussCount': 0, 'lastCuss': time.time()}


            if any([str.lower(word) in str.lower(ctx.content) for word in config['words']]):
                # If the user isn't already logged, create an initial object with a count of 0

                # This assumes time.time() is in seconds. Time in seconds I think so math is : NOW - LastTimeTheyCussed > 1day (86400 seconds ?)
                # Note on code below: If it's been a day since their last cuss, let's just reset them, so we don't punish them for 5 cusses over a month
                if time.time() - self.cussCounter[ctx.author]["lastCuss"] > 86400:
                    self.cussCounter[ctx.author]["cussCount"] = 0

                # Now take action to tally the cuss count and mark the time it happend
                self.cussCounter[ctx.author]["cussCount"] += 1
                self.cussCounter[ctx.author]["lastCuss"] = time.time()

                # writeToActionLog("{date} {author} cuss {message}")

                print("Found a bad word'"+ "' by the author '" + str(ctx.author) + "'. Count is now " + str(
                    self.cussCounter[ctx.author]["cussCount"]) + ".")
                print("User said a bad word, and it wasn't the bot!")
                print("Bad word: " + str(self.cussCounter))

            ## Tally Check


            if any([str.lower(word) in str.lower(ctx.content) for word in config['words']]):
                if self.cussCounter[ctx.author]["cussCount"] >= 1:
                    print("Warning in Chat sent.")
                    botmsg = await ctx.channel.send('{}: {}'.format(ctx.author.mention, config['response']))
                    await ctx.delete()
                    await asyncio.sleep(10)
                    await botmsg.delete()

                if self.cussCounter[ctx.author]["cussCount"] >= 3:
                    blkThreetimes = True
                    print("User said a bad word at least three times.")

                if self.cussCounter[ctx.author]["cussCount"] >= 5:
                    blkThreetimes = False
                    blkFiveTimes = True
                    print("User said a bad word at least five times.")

                    self.cussCounter[ctx.author]["cussCount"] = 0

            if spmcount == 3:
                SpmThreetimes = True
                SpmFiveTimes = False
                print("User spammed at least three times.")

            if spmcount == 5:
                SpmThreetimes = False
                SpmFiveTimes = True
                print("User spammmed at least five times.")

            # Produce the Action
            if incharge and badword or incharge and spmcount >= 3:
                AdminModmessage = (
                    f"""As a Administrator or Moderator of the ITL server, you hold the power of leading this
                    server by example. We want a #positivevibesonly culture in combination of providing an education, impactful
                    experience for all. This bot has counted {self.cussCounter[ctx.author]["cussCount"]} words used on our blocked list and {spmcount}
                    times spammed. If by chance you're forgetting guidelines, please review the #impact-theory-guidelines.
                    If you feel that you got this message in error, please contact @Losstheboss#7859 with questions/concerns.""")
                await ctx.author.send(AdminModmessage)
                print("This is a mod, a reminder of rules was sent.")

            else:
                print("Somehowwenttoelse")

                if SpmThreetimes == True and blkThreetimes == False and blkFiveTimes == False:
                    print("Action: It now hit 3 spam calls")
                    await ctx.author.send(spmDMwarn)

                if SpmFiveTimes == True and blkThreetimes == False and blkFiveTimes == False:
                    print(" Action: It now hit 5 spam calls")
                    await ctx.author.send(spmDMmessage)
                    await ctx.author.add_roles(MutedRole)
                    await ctx.author.remove_roles(StandardRole)





                ## blocked words Action

                if blkThreetimes and SpmThreetimes == False and SpmFiveTimes == False:
                    print("Action:It now hit 3 Blocked Words calls")
                    await ctx.author.send(blockedDMwarn)

                if blkFiveTimes and SpmThreetimes == False and SpmFiveTimes == False:
                    print("Action:It now hit 5 Blocked Words calls")
                    await ctx.author.send(blockedDMmessage)
                    await ctx.author.add_roles(MutedRole)
                    await ctx.author.remove_roles(StandardRole)

                    # writeToActionLog("{date} 'system' userMuted {author} was muted for cussing")

                ## What if both occur?

                if blkThreetimes and SpmThreetimes:
                    print("Action:They're doing both spamming and cussing - Three times")
                    await ctx.author.send(bothDMwarn)

                if blkFiveTimes and SpmFiveTimes:
                    print("Action:They're doing both spamming and cussing - Five times")
                    await ctx.author.send(bothDMmessage)
                    await ctx.author.add_roles(MutedRole)
                    await ctx.author.remove_roles(StandardRole)

                # if self.cussCounter > 5 or spmcount > 5:
                #     print("They should have been muted, or they have been unmuted and still spamming or cussing within "
                #           "the last 5 messages. They may have found a way around this.")


def setup(bot):
    bot.add_cog(PeaceKeeperCog(bot))