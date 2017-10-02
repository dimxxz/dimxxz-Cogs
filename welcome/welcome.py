import discord
import datetime
import re
import time
from discord.ext import commands
from .utils.dataIO import dataIO, fileIO
from .utils import checks
from __main__ import send_cmd_help
import os
import asyncio

#_ modified and improved by dimxxz https://github.com/dimxxz/dimxxz-Cogs
#_ Warning Part forked from aikaterna's imagwelcome cog

default_greeting = "Welcome **{0.name}** to **{1.name}**!"
default_leave = "**{0.name}** has left our server! Bye bye **{0.name}**. Hope you had a good stay!"
default_settings = {"GREETING": default_greeting, "LEAVE": default_leave, "ON": False, "ONL": False, "CHANNEL": None, "WHISPER" : False, "ACCOUNT_WARNINGS": True}

class Welcome:
    """Welcomes new members to the server in the default/set channel"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/welcome/settings.json", "load")


    @commands.group(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def welcomeset(self, ctx):
        """Sets welcome module settings"""
        server = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = default_settings
            self.settings[server.id]["CHANNEL"] = server.default_channel.id
            fileIO("data/welcome/settings.json", "save", self.settings)
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            msg = "```css\n"
            msg += "Greeting: {}\n".format(self.settings[server.id]["GREETING"])
            msg += "Leave: {}\n".format(self.settings[server.id]["LEAVE"])
            msg += "Channel: #{}\n".format(self.get_welcome_channel(server))
            msg += "Welcome ON: {}\n".format(self.settings[server.id]["ON"]) 
            msg += "Leave ON: {}\n".format(self.settings[server.id]["ONL"]) 
            msg += "Whisper: {}\n".format(self.settings[server.id]["WHISPER"])
            msg += "```"
            await self.bot.say(msg)

    @welcomeset.command(pass_context=True)
    async def greeting(self, ctx, *, format_msg):
        """Sets the welcome message format for the server.

                {0} is user
                {1} is server
                Default is set to: 
                    Welcome {0.name} to {1.name}!

                Example formats:
                   1 {0.mention}.. What are you doing here? 
                   2 ***{1.name}***  has a new member! ***{0.name}#{0.discriminator} - {0.id}***
                   3 Someone new joined! Who is it?! D: IS HE HERE TO HURT US?! 
                """
        server = ctx.message.server
        self.settings[server.id]["GREETING"] = format_msg
        fileIO("data/welcome/settings.json", "save", self.settings)
        await self.bot.say("**Done** I've Successfully set the welcome greeting to :\n`{}`".format(format_msg))
        await self.send_testing_msg_join(ctx)

    @welcomeset.command(pass_context=True)
    async def leaving(self, ctx, *, format_msg):
        """Sets the leaving message format for the server.

                {0} is user
                {1} is server
                Default is set to: 
                    {0.name} left {1.name}!

                Example formats:
                   1 {0.mention}.. left just now? 
                   2 ***{1.name}***  lost a member! ***{0.name}#{0.discriminator} - {0.id}***
                   3 Someone just left! Who was it?! D:?!"""
        server = ctx.message.server
        self.settings[server.id]["LEAVE"] = format_msg
        fileIO("data/welcome/settings.json", "save", self.settings)
        await self.bot.say("**Done** I've Successfully set the leaving message to :\n`{}`".format(format_msg))
        await self.send_testing_msg_leave(ctx)

    @welcomeset.command(pass_context=True)
    async def togglej(self, ctx):
        """Turns on/off welcoming new users to the server"""
        server = ctx.message.server
        self.settings[server.id]["ON"] = not self.settings[server.id]["ON"]
        if self.settings[server.id]["ON"]:
            await self.bot.say("**I will now welcome New users.**")
            await self.send_testing_msg_join(ctx)
        else:
            await self.bot.say("**I will no longer welcome new users.**")
        fileIO("data/welcome/settings.json", "save", self.settings)
		
    @welcomeset.command(pass_context=True)
    async def togglel(self, ctx):
        """Turns on/off leaving message trigger"""
        server = ctx.message.server
        self.settings[server.id]["ONL"] = not self.settings[server.id]["ONL"]
        if self.settings[server.id]["ONL"]:
            await self.bot.say("**I will now send the Leaving message.**")
            await self.send_testing_msg_leave(ctx)
        else:
            await self.bot.say("**I will no longer send the Leaving message.**")
        fileIO("data/welcome/settings.json", "save", self.settings)

    @welcomeset.command(pass_context=True)
    async def channel(self, ctx, channel : discord.Channel=None): 
        """Sets the channel to send the welcome message

        If channel isn't specified, the server's default channel will be used"""
        server = ctx.message.server
        if channel == None:
            channel = ctx.message.server.default_channel
        if not server.get_member(self.bot.user.id).permissions_in(channel).send_messages:
            await self.bot.say(":bangbang::no_good:**I am not capable of sending messages to** ***{0.mention}***:x:".format(channel))
            return
        self.settings[server.id]["CHANNEL"] = channel.id
        fileIO("data/welcome/settings.json", "save", self.settings)
        channel = self.get_welcome_channel(server)
        await self.bot.send_message(channel,"**I will now send welcome messages to** ***{0.mention}**".format(channel))
        await self.send_testing_msg(ctx)

    @welcomeset.command(pass_context=True)
    async def whisper(self, ctx, choice : str=None):
        """Sets whether or not a DM is sent to the new user
        
        Options:
            off - turns off DMs to users
            only - only send a DM to the user, don't send a welcome to the channel
            both - send a message to both the user and the channel

        If Option isn't specified, toggles between 'off' and 'only'"""
        options = {"off": False, "only": True, "both": "BOTH"}
        server = ctx.message.server
        if choice == None:
            self.settings[server.id]["WHISPER"] = not self.settings[server.id]["WHISPER"]
        elif choice.lower() not in options:
            await send_cmd_help(ctx)
            return
        else:
            self.settings[server.id]["WHISPER"] = options[choice.lower()]
        fileIO("data/welcome/settings.json", "save", self.settings)
        channel = self.get_welcome_channel(server)
        if not self.settings[server.id]["WHISPER"]:
            await self.bot.say("**I will no longer send DMs to new users**")
        elif self.settings[server.id]["WHISPER"] == "BOTH":
            await self.bot.send_message(channel, "**I will now send welcome messages to** ***{0.mention}*** **as well as to the new user in a DM**".format(channel))
        else:
            await self.bot.send_message(channel, "I will keep sending welcome messages in **DM** :D.".format(channel))
        await self.send_testing_msg(ctx)


    async def on_server_join(self, server):
        greetingmsg = "Welcome {0.mention} to **{1.name}**!"
        leavemsg = "**{0.name}** has left our server! Bye bye **{0.name}**. Hope you had a good stay!"
        def_settings = {"GREETING": greetingmsg, "LEAVE": leavemsg, "ON": False, "ONL": False, "CHANNEL": None, "WHISPER": False}
        if server.id not in self.settings:
            self.settings[server.id] = def_settings
            self.settings[server.id]["CHANNEL"] = server.default_channel.id
            fileIO("data/welcome/settings.json", "save", self.settings)
            return
	
    async def member_join(self, member):
        server = member.server
        greetingmsg = "Welcome {0.mention} to **{1.name}**!"
        leavemsg = "**{0.name}** has left our server! Bye bye **{0.name}**. Hope you had a good stay!"
        def_settings = {"GREETING": greetingmsg, "LEAVE": leavemsg, "ON": False, "ONL": False, "CHANNEL": None, "WHISPER": False, "ACCOUNT_WARNINGS": True}
        memberjoin = self.settings[server.id]["GREETING"].format(member, server)
        e = discord.Embed(title="Joined", description=memberjoin, colour=discord.Colour.blue())
        e.set_thumbnail(url=member.avatar_url)
        if server.id not in self.settings:
            self.settings[server.id] = def_settings
            self.settings[server.id]["CHANNEL"] = server.default_channel.id
            fileIO("data/welcome/settings.json", "save", self.settings)
        if not self.settings[server.id]["ON"]:
            return
        if server == None:
            print("Server is None. Private Message or some new fangled Discord thing?.. Anyways there be an error, the user was {}".format(member.name))
            return
        channel = self.get_welcome_channel(server)
        if channel is None:
            print('welcome.py: Channel not found. It was most likely deleted. User joined: {}'.format(member.name))
            return
        if self.settings[server.id]["WHISPER"]:
            await self.bot.send_message(member, embed=e)
        if self.settings[server.id]["WHISPER"] != True and self.speak_permissions(server):
            await self.bot.send_message(channel, embed=e)
        else:
            print("Permissions Error. User that joined: {0.name}".format(member))
            print("Bot doesn't have permissions to send messages to {0.name}'s #{1.name} channel".format(server,channel))
        date_join = datetime.datetime.strptime(str(member.created_at), "%Y-%m-%d %H:%M:%S.%f")
        date_now = datetime.datetime.now(datetime.timezone.utc)
        date_now = date_now.replace(tzinfo=None)
        since_join = date_now - date_join
        msgx = "\N{WARNING SIGN} This account was created less than a week ago (" + str(since_join.days) + " days ago)"
        e2 = discord.Embed(description=msgx, colour=discord.Colour.red())
        if since_join.days < 7 and self.settings[server.id]["ACCOUNT_WARNINGS"]:
            await self.bot.send_message(channel, embed=e2)
			
    async def member_remove(self, member):
        server = member.server
        greetingmsg = "Welcome {0.mention} to **{1.name}**!"
        leavemsg = "**{0.name}** has left our server! Bye bye **{0.name}**. Hope you had a good stay!"
        def_settings = {"GREETING": greetingmsg, "LEAVE": leavemsg, "ON": False, "ONL": False, "CHANNEL": None, "WHISPER": False, "ACCOUNT_WARNINGS": True}
        memberleave = self.settings[server.id]["LEAVE"].format(member, server)
        e = discord.Embed(title="Left", description=memberleave, colour=discord.Colour.red())
        e.set_thumbnail(url=member.avatar_url)
        if server.id not in self.settings:
            self.settings[server.id] = def_settings
            self.settings[server.id]["CHANNEL"] = server.default_channel.id
            fileIO("data/welcome/settings.json", "save", self.settings)
        if not self.settings[server.id]["ONL"]:
            return
        if server == None:
            print("Server is None. Private Message or some new fangled Discord thing?.. Anyways there be an error, the user was {}".format(member.name))
            return
        channel = self.get_welcome_channel(server)
        if channel is None:
            print('welcome.py: Channel not found. It was most likely deleted. User left: {}'.format(member.name))
            return
        if self.settings[server.id]["WHISPER"]:
            await self.bot.send_message(member, embed=e)
        if self.settings[server.id]["WHISPER"] != True and self.speak_permissions(server):
            await self.bot.send_message(channel, embed=e)
        else:
            print("Permissions Error. User that left: {0.name}".format(member))
            print("Bot doesn't have permissions to send messages to {0.name}'s #{1.name} channel".format(server,channel))


    def get_welcome_channel(self, server):
        try:
            return server.get_channel(self.settings[server.id]["CHANNEL"])
        except:
            return None

    def speak_permissions(self, server):
        channel = self.get_welcome_channel(server)
        if channel is None:
            return False
        return server.get_member(self.bot.user.id).permissions_in(channel).send_messages

    async def send_testing_msg_join(self, ctx):
        server = ctx.message.server
        channel = self.get_welcome_channel(server)
        memberjoin = self.settings[server.id]["GREETING"].format(ctx.message.author, server)
        e = discord.Embed(title="Joined", description=memberjoin, colour=discord.Colour.blue())
        e.set_footer(text="This is a Test message!")
        e.set_thumbnail(url=ctx.message.author.avatar_url)
        if channel is None:
            await self.bot.send_message(ctx.message.channel, ":bangbang::x:**I cannot find the specified Channel** :bangbang:")
            return
        await self.bot.send_message(ctx.message.channel, "**Sending A testing message to** ***{}***".format(channel))
        if self.speak_permissions(server):
            if self.settings[server.id]["WHISPER"]:
                await self.bot.send_message(ctx.message.author, embed=e)
                #await self.bot.send_message(ctx.message.author, self.settings[server.id]["GREETING"].format(ctx.message.author,server))
            if self.settings[server.id]["WHISPER"] != True:
                await self.bot.send_message(channel, embed=e)
                #await self.bot.send_message(channel, self.settings[server.id]["GREETING"].format(ctx.message.author,server))
        else: 
            await self.bot.send_message(ctx.message.channel, ":bangbang::no_good:**I am not capable of sending messages to** ***{0.mention}***:x:".format(channel))

    async def send_testing_msg_leave(self, ctx):
        server = ctx.message.server
        channel = self.get_welcome_channel(server)
        memberleave = self.settings[server.id]["LEAVE"].format(ctx.message.author, server)
        e = discord.Embed(title="Left", description=memberleave, colour=discord.Colour.red())
        e.set_footer(text="This is a Test message!")
        e.set_thumbnail(url=ctx.message.author.avatar_url)
        if channel is None:
            await self.bot.send_message(ctx.message.channel, ":bangbang::x:**I cannot find the specified Channel** :bangbang:")
            return
        await self.bot.send_message(ctx.message.channel, "**Sending A testing message to** ***{}***".format(channel))
        if self.speak_permissions(server):
            if self.settings[server.id]["WHISPER"]:
                await self.bot.send_message(ctx.message.author, embed=e)
                #await self.bot.send_message(ctx.message.author, self.settings[server.id]["LEAVE"].format(ctx.message.author,server))
            if self.settings[server.id]["WHISPER"] != True:
                await self.bot.send_message(channel, embed=e)
                #await self.bot.send_message(channel, self.settings[server.id]["LEAVE"].format(ctx.message.author,server))
        else: 
            await self.bot.send_message(ctx.message.channel, ":bangbang::no_good:**I am not capable of sending messages to** ***{0.mention}***:x:".format(channel))


def check_folders():
    if not os.path.exists("data/welcome"):
        print("Creating data/welcome folder...")
        os.makedirs("data/welcome")

def check_files():
    f = "data/welcome/settings.json"
    if not fileIO(f, "check"):
        print("Creating welcome settings.json...")
        fileIO(f, "save", {})
    else: #consistency check
        current = fileIO(f, "load")
        for k,v in current.items():
            if v.keys() != default_settings.keys():
                for key in default_settings.keys():
                    if key not in v.keys():
                        current[k][key] = default_settings[key]
                        print("Adding " + str(key) + " field to welcome settings.json")
        fileIO(f, "save", current)

def setup(bot):
    check_folders()
    check_files()
    n = Welcome(bot)
    bot.add_listener(n.member_join,"on_member_join")
    bot.add_listener(n.member_remove, "on_member_remove")
    bot.add_cog(n)
