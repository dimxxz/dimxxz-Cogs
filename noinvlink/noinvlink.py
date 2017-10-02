import discord
import os
from __main__ import settings
from random import choice as randchoice
from discord.ext import commands
from .utils import checks
from cogs.utils.dataIO import dataIO, fileIO

___author___ = "dimxxz"

# written by dimxxz  https://github.com/dimxxz/dimxxz-Cogs

class invlinkblock:
    def __init__(self, bot):
        self.bot = bot
        self.owner = '<!{}>'.format(settings.owner)
        self.settings = dataIO.load_json("data/invlinkblock/settings.json")

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def invblock(self, ctx):
        """Turns on/off Discord Invite-link Blocker"""
        server = ctx.message.server
        channel = ctx.message.channel
        if server.id not in self.settings:
            self.settings[server.id] = {'ON': 0}
            self.save_settings()
        else:
            pass
        if self.settings[server.id]['ON'] == 1:
            self.settings[server.id]['ON'] = self.settings[server.id]['ON'] - 1
            self.save_settings()
            e = discord.Embed(title="Discord Invite Link Blocker",
                              description="Invite-link Block is **OFF** now."
                                          "", colour=discord.Colour.green())
            await self.bot.send_message(channel, embed = e)
            return
        elif self.settings[server.id]['ON'] == 0:
            self.settings[server.id]['ON'] = self.settings[server.id]['ON'] + 1
            self.save_settings()
            e = discord.Embed(title="Discord Invite Link Blocker",
                              description="Invite-link Block is **ON** now."
                                          "", colour=discord.Colour.green())
            await self.bot.send_message(channel, embed = e)
            return
		
    async def listener(self, message):
        channel = message.channel
        server = message.server
        e = discord.Embed(title="Discord Invite Link Blocker",
                          description="**STOP** posting invite links!!!!"
                                      "", colour=discord.Colour.red())
        msg = "**STOP** posting invite links!!!!"
        #if server.id not in self.settings:
        #    self.settings[server.id] = {'ON': 0}
        #    self.save_settings()
        #else:
        #    pass
        if self.settings[message.server.id]['ON'] == 1:
            if message.author.id != self.bot.user.id:
                if message.author.id != server.owner.id:
                    if 'http://discord.gg/' in message.content.lower() or 'https://discord' in message.content.lower():
                        try:
                            await self.bot.send_message(channel, message.author.mention + " :no_entry: ")
                            await self.bot.send_message(channel, embed = e)
                            await self.bot.delete_message(message)
                        except discord.Forbidden:
                            await self.bot.send_message(channel, message.author.mention + " :no_entry: ")
                            await self.bot.send_message(channel, msg)
                            await self.bot.delete_message(message)
                    elif 'https://discord.me' in message.content.lower() or 'http://discord' in message.content.lower():
                        try:
                            await self.bot.send_message(channel, message.author.mention + " :no_entry: ")
                            await self.bot.send_message(channel, embed = e)
                            await self.bot.delete_message(message)
                        except discord.Forbidden:
                            await self.bot.send_message(channel, message.author.mention + " :no_entry: ")
                            await self.bot.send_message(channel, msg)
                            await self.bot.delete_message(message)
        elif self.settings[server.id]['ON'] == 0:
            pass
			
    async def on_server_join(self, server):
        if server.id not in self.settings:
            self.settings[server.id] = {'ON': 0}
            self.save_settings()
        else:
            pass
			
    def save_settings(self):
        dataIO.save_json("data/invlinkblock/settings.json", self.settings)

def check_folders():
    if not os.path.exists("data/invlinkblock"):
        print("Creating data/invlinkblock folder...")
        os.makedirs("data/invlinkblock")

def check_files():
    if not os.path.exists("data/invlinkblock/settings.json"):
        print("Creating data/invlinkblock/settings.json file...")
        dataIO.save_json("data/invlinkblock/settings.json", {})

def setup(bot):
    check_folders()
    check_files()
    n = invlinkblock(bot)
    bot.add_listener(n.listener, "on_message")
    bot.add_cog(n)
