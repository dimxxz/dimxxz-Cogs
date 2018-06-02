import discord
from discord.ext import commands
from .utils import checks
import urllib.request
import urllib.parse
from cogs.utils.dataIO import dataIO
from random import choice as randchoice
from cogs.utils.chat_formatting import box, pagify
import re
import os

__author__ = "dimxxz - https://github.com/dimxxz/dimxxz-Cogs"

class YoutubeSearch:
    """Searches Youtube for stuff"""

    def __init__(self, bot):
        self.bot = bot
        self.songs = dataIO.load_json("data/songs/songs.json")

    @commands.group(pass_context=True, no_pm=True)
    async def yts(self, ctx):
        """Youtube Search Overview"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)


    @yts.command(name="search", pass_context=True, no_pm=True)
    async def ytsearch(self, ctx, *, song):
        """Search Youtube videos"""
        for num in song:
            if str(num).isdigit():
                num_x = int(str(num))
                break
            else:
                res = "0"
                num_x = int(str(res))
                break
        try:
            query_string = urllib.parse.urlencode({"search_query": song})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            await self.bot.say("http://www.youtube.com/watch?v=" + search_results[num_x])
        except IndexError:
            await self.bot.say("Nothing found!")

    @yts.command(name="give", pass_context=True, no_pm=True)
    async def ytsong(self, ctx):
        """Gives a random song"""
        song = randchoice(self.songs)
        await ctx.invoke(self.ytsearch, song=song)

    @yts.command(name="add", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def ytsadd(self, ctx, *, songname):
        """Adds a youtube song name."""
        if songname in self.songs:
            await self.bot.say("That song is already in the list!")
        else:
            self.songs.append(songname)
            self.save_settings()
            await self.bot.say("Song added to the list!")

    @yts.command(name="rem", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def ytsdel(self, ctx, *, songname):
        """Removes a youtube song name."""
        if songname not in self.songs:
            await self.bot.say("That song is not in the list!")
        else:
            self.songs.remove(songname)
            self.save_settings()
            await self.bot.say("Song removed!")

    @yts.command(name="list", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def ytslist(self, ctx):
        """Lists all song names."""
        songs = ""
        for song in self.songs:
            songs += song + "\n"
        for page in pagify(songs, delims=["\n"]):
            await self.bot.say(box(page))

    def save_settings(self):
        dataIO.save_json("data/songs/songs.json", self.songs)


def check_folders():
    if not os.path.exists("data/songs"):
        print("Creating data/songs folder...")
        os.makedirs("data/songs")


def check_files():
    if not os.path.exists("data/songs/songs.json"):
        print("Creating data/songs/songs.json file...")
        dataIO.save_json("data/songs/songs.json", [])

def setup(bot):
    check_folders()
    check_files()
    n = YoutubeSearch(bot)
    bot.add_cog(n)
