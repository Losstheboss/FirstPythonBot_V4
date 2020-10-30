from discord.ext import commands
import discord

import asyncio


class PeaceKeeperCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        wchannel = member.guild.get_channel(651459232453099521)
        if member.guild.id != 651457715474006017:
            return

        try:
            await wchannel.send(
                f"""Welcome to the Impact Theory League Discord Server, {member.mention}! 
                Please go to the #impact-theory-guidelines channel in order to interact with the server. 
                We currently have {member.guild.member_count} that have joined the Impact Theory Discord server!""",
            )
            initial_message = await member.send(
                f"""Welcome to the Impact Theory League Discord Server, {member.mention}! 
                Please go to the #impact-theory-guidelines channel in order to interact with the server. 
                We currently have {member.guild.member_count} that have joined the Impact Theory Discord server!""",
                delete_after=60 * 15  # They have 15 minutes to accept
            )
        except discord.HTTPException:
            print(f'Could not DM {member.name} (ID: {member.id}) to accept terms.')

        role = member.guild.get_role(651599119239872533)
        await member.add_roles(role)

        try:
            def check(p):  # `p` is short for payload
                return p.message_id == 651606717183950858 \
                    and p.user_id == member.id \
                   # and str(p.emoji) == '👌'  # I am not sure if this is the correct string for the reaction

            print("User Reacted.")
            payload = await self.bot.wait_for('raw_reaction_add',
                                              check=check)
                                              #timeout=60 * 15)  # They have 15 minutes to accept
            if str(payload.emoji) == ':ok_hand:':
                print(str(payload.emoji))

        except asyncio.TimeoutError:
            print(f'{member.name} (ID: {member.id}) Did not accept terms, kicked them.')
            return await member.kick()  # Member did not accept guidelines, kicking them.

        await initial_message.delete()
        await member.remove_roles(role)
        role = member.guild.get_role(651599264018857998)
        await member.add_roles(role)
        print(f'{member.name} (ID: {member.id}) Has accepted terms, given them {role.name}')
        await member.send(
            f"""Thanks for accepting our guidelines, {member.mention}! 
            You should see the server channels appear within a few minutes.""")


def setup(bot):
    bot.add_cog(PeaceKeeperCog(bot))