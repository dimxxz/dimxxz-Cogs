import discord
from discord.ext import commands
import os
from .utils import checks
from __main__ import settings
from cogs.utils.dataIO import dataIO
import asyncio

#written by PlanetTeamSpeakk/PTSCogs https://github.com/PlanetTeamSpeakk/PTSCogs
#
#improved and rewritten by dimxxz https://github.com/dimxxz/dimxxz-Cogs
class Marry:
    """Marry your loved one."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/marry/settings.json")

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(pass_context=True, no_pm=True)
    async def marry(self, ctx, yourlovedone:discord.Member):
        """Now you can finally marry your loved one."""
        if ctx.message.server.id not in self.settings:
            self.settings[ctx.message.server.id] = {'marry_limit': 1, 'disabled': False}
            self.save_settings()
        if yourlovedone.id not in self.settings[ctx.message.server.id]:
            self.settings[ctx.message.server.id][yourlovedone.id] = 0
            self.save_settings()
        if ctx.message.author.id not in self.settings[ctx.message.server.id]:
            self.settings[ctx.message.server.id][ctx.message.author.id] = 0
            self.save_settings()
        if 'disabled' not in self.settings[ctx.message.server.id]:
            self.settings[ctx.message.server.id]['disabled'] = False
            self.save_settings()
        if not self.settings[ctx.message.server.id]['disabled']:
            if yourlovedone.id == ctx.message.author.id:
                await self.bot.say("You can't marry yourself, that would be weird wouldn't it?")
                return
            elif yourlovedone.id == ctx.message.server.me.id:
                if ctx.message.author.id != settings.owner:
                    await self.bot.say("I'd only marry my owner.")
                    return
            for role in ctx.message.author.roles:
                if ctx.message.author.name in role.name:
                    if " ❤ " in role.name:
                        if yourlovedone.name in role.name:
                            await self.bot.say("You're already married with this person.")
                            return
        else:
            await self.bot.say("Marriages are disabled in this server.")
            return
        times_married = 0
        if self.settings[ctx.message.server.id][ctx.message.author.id] is not 0:
            times_married = times_married + self.settings[ctx.message.server.id][ctx.message.author.id]
            if times_married >= self.settings[ctx.message.server.id]['marry_limit']:
                await self.bot.say("You have reached the marry limit ({}).".format(self.settings[ctx.message.server.id]['marry_limit']))
                self.settings[ctx.message.server.id][ctx.message.author.id] = times_married
                self.save_settings()
                return
            times_married = 0
			
        elif self.settings[ctx.message.server.id][yourlovedone.id] is not 0:
            times_married = times_married + self.settings[ctx.message.server.id][yourlovedone.id]
            if times_married >= self.settings[ctx.message.server.id]['marry_limit']:
                await self.bot.say("Your loved one has reached the marry limit ({}).".format(self.settings[ctx.message.server.id]['marry_limit']))
                return
        await self.bot.say("{} do you take {} as your husband/wife? (yes/no)".format(yourlovedone.mention, ctx.message.author.mention))
        answer = await self.bot.wait_for_message(timeout=60, author=yourlovedone)
        if answer is None:
            await self.bot.say("The user you tried to marry didn't respond, I'm sorry.")
            return
        elif not answer.content.lower().startswith('yes'):#"yes" not in answer.content.lower():
            await self.bot.say("The user you tried to marry didn't say yes, I'm sorry.")
            return
        try:
            married_role = await self.bot.create_role(server=ctx.message.server, name="{} ❤ {}".format(ctx.message.author.name, yourlovedone.name), colour=discord.Colour(value=0XFF00EE))
        except discord.Forbidden:
            await self.bot.say("I do not have the `manage roles` permission, you can't marry untill I do.")
            return
        except Exception as e:
            await self.bot.say("Couldn't make your loved role, unknown error occured,\n{}.".format(e))
            return
        await self.bot.add_roles(ctx.message.author, married_role)
        await self.bot.add_roles(yourlovedone, married_role)
        await self.bot.send_message(ctx.message.author, "You married **{0}** in **{1}**\nYour divorce id is `{2}`!\nTo divorce type `{3}divorce {2} @{0}`.\nIf anything fails, ask your Server Admin to use `{3}forcedivorce {2}` !".format(str(yourlovedone), ctx.message.server.name, married_role.id, ctx.prefix))
        if not yourlovedone.bot:
            await self.bot.send_message(yourlovedone, "You married **{0}** in **{1}**\nYour divorce id is `{2}`!\nTo divorce type `{3}divorce {2} @{0}`.\nIf anything fails, ask your Server Admin to use `{3}forcedivorce {2}` ".format(str(ctx.message.author), ctx.message.server.name, married_role.id, ctx.prefix))
        else:
            pass
        marchan = discord.utils.find(lambda c: c.name == 'marriage', ctx.message.server.channels)
        if marchan:
            self.settings[ctx.message.server.id][ctx.message.author.id] = self.settings[ctx.message.server.id][ctx.message.author.id] + 1
            self.settings[ctx.message.server.id][yourlovedone.id] = self.settings[ctx.message.server.id][yourlovedone.id] + 1
            self.save_settings()
            await self.bot.say("You're now married, congratulations!")
            await self.bot.send_message(marchan, "{} married {} congratulations!".format(ctx.message.author.mention, yourlovedone.mention))
        else:
            try:
                marchan = await self.bot.create_channel(ctx.message.server, "marriage")
                await self.bot.say("You're now married, congratulations!")
                await self.bot.send_message(marchan, "{} married {} congratulations!".format(ctx.message.author.mention, yourlovedone.mention))
                self.settings[ctx.message.server.id][ctx.message.author.id] = self.settings[ctx.message.server.id][ctx.message.author.id] + 1
                self.settings[ctx.message.server.id][yourlovedone.id] = self.settings[ctx.message.server.id][yourlovedone.id] + 1
                self.save_settings()
            except:
                await self.bot.say("{} married {}, congratulations! I suggest telling the server owner or moderators to make a #marriage channel though.".format(ctx.message.author.mention, yourlovedone.mention))
        return

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(pass_context=True, no_pm=True)
    async def marryit(self, ctx, thing):
        """Now you can finally marry your loved things! That's some weird fetish right there!"""
        if ctx.message.server.id not in self.settings:
            self.settings[ctx.message.server.id] = {'marry_limit': 1, 'disabled': False}
            self.save_settings()
        if ctx.message.author.id not in self.settings[ctx.message.server.id]:
            self.settings[ctx.message.server.id][ctx.message.author.id] = 0
            self.save_settings()
        if 'disabled' not in self.settings[ctx.message.server.id]:
            self.settings[ctx.message.server.id]['disabled'] = False
            self.save_settings()
        if not self.settings[ctx.message.server.id]['disabled']:
            if thing == ctx.message.author.id:
                await self.bot.say("You can't marry yourself, that would be weird wouldn't it?")
                return
            elif thing == ctx.message.server.me.mention:
                if ctx.message.author.id != settings.owner:
                    await self.bot.say("I'd only marry my owner.")
                    return
            elif thing == ("<@333054706052235265>"):
                if ctx.message.author.id != settings.owner:
                    await self.bot.say("Devil Miku will only marry her owner.")
                    return
        else:
            await self.bot.say("Marriages are disabled in this server.")
            return
        times_married = 0
        if self.settings[ctx.message.server.id][ctx.message.author.id] is not 0:
            times_married = times_married + self.settings[ctx.message.server.id][ctx.message.author.id]
            if times_married >= self.settings[ctx.message.server.id]['marry_limit']:
                await self.bot.say("You have reached the marry limit ({}).".format(self.settings[ctx.message.server.id]['marry_limit']))
                self.settings[ctx.message.server.id][ctx.message.author.id] = times_married
                self.save_settings()
                return
        try:
            married_role = await self.bot.create_role(server=ctx.message.server, name="{} ❤ {}".format(ctx.message.author.name, thing), colour=discord.Colour(value=0XFF00EE))
        except discord.Forbidden:
            await self.bot.say("I do not have the `manage roles` permission, you can't marry untill I do.")
            return
        except Exception as e:
            await self.bot.say("Couldn't make your loved role, unknown error occured,\n{}.".format(e))
            return
        await self.bot.add_roles(ctx.message.author, married_role)
        await self.bot.send_message(ctx.message.author, "You married **{0}** in **{1}**\nYour divorce id is `{2}`!\nTo divorce type `{3}divorce {2} @{0}`.\nIf anything fails, ask your Server Admin to use `{3}forcedivorce {2}` !".format(thing, ctx.message.server.name, married_role.id, ctx.prefix))
        marchan = discord.utils.find(lambda c: c.name == 'marriage', ctx.message.server.channels)
        if marchan:
            await self.bot.say("You're now married, congratulations!")
            await self.bot.send_message(marchan, "{} married **{}** congratulations!".format(ctx.message.author.mention, thing))
        else:
            try:
                marchan = await self.bot.create_channel(ctx.message.server, "marriage")
                await self.bot.say("You're now married, congratulations!")
                await self.bot.send_message(marchan, "{} married **{}** congratulations!".format(ctx.message.author.mention, thing))
            except:
                await self.bot.say("{} married **{}**, congratulations! I suggest telling the server owner or moderators to make a #marriage channel though.".format(ctx.message.author.mention, thing))
        return

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def forcemarry(self, ctx, person:discord.Member, lovedone:discord.Member):
        """Now you can finally force marry 2 users."""
        if (ctx.message.server.id not in self.settings) or ("marry_limit" not in self.settings[ctx.message.server.id]):
            self.settings[ctx.message.server.id] = {'marry_limit': 0, 'disabled': False}
            self.save_settings()
        if lovedone.id not in self.settings[ctx.message.server.id]:
            self.settings[ctx.message.server.id][lovedone.id] = 0
            self.save_settings()
        if person.id not in self.settings[ctx.message.server.id]:
            self.settings[ctx.message.server.id][person.id] = 0
            self.save_settings()
        if 'disabled' not in self.settings[ctx.message.server.id]:
            self.settings[ctx.message.server.id]['disabled'] = False
            self.save_settings()
        if not self.settings[ctx.message.server.id]['disabled']:
            if lovedone.id == person.id:
                await self.bot.say("You can't let someone marry him/herself that would be weird wouldn't it?")
                return
            for role in person.roles:
                if person.name in role.name:
                    if " ❤ " in role.name:
                        if lovedone.name in role.name:
                            await self.bot.say("This person is already married with his/her loved one.")
                            return
            if lovedone.id == ctx.message.server.me.id:
                if ctx.message.author.id != settings.owner:
                    await self.bot.say("I'd only marry my owner.")
                    return
            elif person.id == ctx.message.server.me.id:
                if ctx.message.author.id != settings.owner:
                    await self.bot.say("I'd only marry my owner.")
                    return
        else:
            await self.bot.say("Marriages are disabled in this server.")
            return
        times_married = 0
        if self.settings[ctx.message.server.id][person.id] is not 0:
            times_married = times_married + self.settings[ctx.message.server.id][person.id]
            if times_married >= self.settings[ctx.message.server.id]['marry_limit']:
                await self.bot.say("You have reached the marry limit ({}).".format(self.settings[ctx.message.server.id]['marry_limit']))
                self.settings[ctx.message.server.id][person.id] = times_married
                self.save_settings()
                return
            times_married = 0
        elif self.settings[ctx.message.server.id][lovedone.id] is not 0:
            times_married = times_married + self.settings[ctx.message.server.id][lovedone.id]
            if times_married >= self.settings[ctx.message.server.id]['marry_limit']:
                await self.bot.say("The loved one has reached the marry limit ({}).".format(self.settings[ctx.message.server.id]['marry_limit']))
                return
        try:
            married_role = await self.bot.create_role(server=ctx.message.server, name="{} ❤ {}".format(person.name, lovedone.name), colour=discord.Colour(value=0XFF00EE))
        except discord.Forbidden:
            await self.bot.say("I do not have the `manage roles` permission, you can't marry untill I do.")
            return
        except Exception as e:
            await self.bot.say("Couldn't make your loved role, unknown error occured,\n{}.".format(e))
            return
        await self.bot.add_roles(person, married_role)
        await self.bot.add_roles(lovedone, married_role)
        try:
            await self.bot.send_message(person, "**{0}** married you to **{1}** in **{2}**.\nYour divorce id is `{3}`!\nTo divorce type `{4}divorce {3}`.\nIf anything fails, ask your server Admin to use `{3}forcedivorce {2}` !".format(ctx.message.author.name, str(lovedone), ctx.message.server.name, married_role.id, ctx.prefix))
        except:
            pass
        try:
            await self.bot.send_message(lovedone, "**{0}** married you to **{1}** in **{2}**.\nYour divorce id is `{3}`!\nTo divorce type `{4}divorce {3}`.\nIf anything fails, ask your server Admin to use `{3}forcedivorce {2}` !".format(ctx.message.author.name, str(person), ctx.message.server.name, married_role.id, ctx.prefix))
        except:
            pass
        else:
            pass
        marchan = discord.utils.find(lambda c: c.name == 'marriage', ctx.message.server.channels)
        if marchan:
            await self.bot.say("They're now married, congratulations!")
            await self.bot.send_message(marchan, "{} was forced to marry {}.".format(person.mention, lovedone.mention))
            self.settings[ctx.message.server.id][person.id] = self.settings[ctx.message.server.id][person.id] + 1
            self.settings[ctx.message.server.id][lovedone.id] = self.settings[ctx.message.server.id][lovedone.id] + 1
            self.save_settings()
        else:
            try:
                marchan = await self.bot.create_channel(ctx.message.server, "marriage")
                await self.bot.say("They're now married, congratulations!")
                await self.bot.send_message(marchan, "{} was forced to marry {}.".format(person.mention, lovedone.mention))
                self.settings[ctx.message.server.id][person.id] = self.settings[ctx.message.server.id][person.id] + 1
                self.settings[ctx.message.server.id][lovedone.id] = self.settings[ctx.message.server.id][lovedone.id] + 1
                self.save_settings()
            except:
                await self.bot.say("{} married {}, congratulations! I suggest telling the server owner or moderators to make a #marriage channel though.".format(person.mention, lovedone.mention))
                return
        
    @commands.command(pass_context=True, no_pm=True)
    async def divorce(self, ctx, divorce_id, user: discord.Member=None):
        """Divorce your ex."""
        times_married = self.settings[ctx.message.server.id][ctx.message.author.id]
        author_id = ctx.message.author
        try:
            married_role = discord.utils.get(ctx.message.server.roles, id=divorce_id)
            if not "❤" in married_role.name.split():
                await self.bot.say("That's not a valid ID.")
                return
            elif not ctx.message.author.name in married_role.name.split():
                await self.bot.say("That's not a valid ID")
            else:
                pass
                if author_id.name in married_role.name.split():
                    #await self.bot.say("ok authorid found. married {}".format(times_married))
                    if user.name in married_role.name.split():
                        times_married2 = self.settings[ctx.message.server.id][user.id]
                        #await self.bot.say("ok userid found. married {}".format(times_married2))
                        await self.bot.delete_role(ctx.message.server, married_role)
                        marchan = discord.utils.find(lambda c: c.name == 'marriage', ctx.message.server.channels)
                        if marchan:
                            await self.bot.say("You're now divorced.")
                            await self.bot.send_message(marchan, "{} divorced ID `{}`.".format(ctx.message.author.mention, divorce_id))
                            times_married = times_married - self.settings[ctx.message.server.id][ctx.message.author.id]
                            times_married2 = times_married2 - self.settings[ctx.message.server.id][user.id]
                            self.settings[ctx.message.server.id][ctx.message.author.id] = times_married
                            self.settings[ctx.message.server.id][user.id] = times_married2
                            self.save_settings()
                        else:
                            try:
                                marchan = await self.bot.create_channel(ctx.message.server, "marriage")
                                await self.bot.say("You're now divorced.")
                                await self.bot.send_message(marchan, "{} divorced ID `{}`.".format(ctx.message.author.mention, divorce_id))
                                times_married = times_married - self.settings[ctx.message.server.id][ctx.message.author.id]
                                times_married2 = times_married2 - self.settings[ctx.message.server.id][user.id]
                                self.settings[ctx.message.server.id][ctx.message.author.id] = times_married
                                self.settings[ctx.message.server.id][user.id] = times_married2
                                self.save_settings()
                            except:
                                await self.bot.say("You're now divorced! I suggest telling the server owner or moderators to make a #marriage channel though.")
                                return
        except discord.Forbidden:
            await self.bot.say("I do not have the `manage roles` permission, I need it to divorce you.")
            return
        except:
            await self.bot.say("That's not a valid ID.")
            return

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def forcedivorce(self, ctx, divorce_id):
        """Divorce your ex. This command should be used in case when the husband/wife left the server or the regular divorce didn't work!"""
        try:
            married_role = discord.utils.get(ctx.message.server.roles, id=divorce_id)
            if not "❤" in married_role.name.split():
                await self.bot.say("That's not a valid ID.")
                return
            elif not ctx.message.author.name in married_role.name.split():
                await self.bot.say("That's not a valid ID")
            else:
                pass
            await self.bot.delete_role(ctx.message.server, married_role)
            marchan = discord.utils.find(lambda c: c.name == 'marriage', ctx.message.server.channels)
            if marchan:
                await self.bot.say("You're now divorced.")
                await self.bot.send_message(marchan, "{} divorced ID `{}`.".format(ctx.message.author.mention, divorce_id))
            else:
                try:
                    marchan = await self.bot.create_channel(ctx.message.server, "marriage")
                    await self.bot.say("You're now divorced.")
                    await self.bot.send_message(marchan, "{} divorced ID `{}`.".format(ctx.message.author.mention, divorce_id))
                except:
                    await self.bot.say("You're now divorced! I suggest telling the server owner or moderators to make a #marriage channel though.")
                    return
        except discord.Forbidden:
            await self.bot.say("I do not have the `manage roles` permission, I need it to divorce you.")
            return
        except:
            await self.bot.say("That's not a valid ID.")
            return
            
    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def setmarrylimit(self, ctx, times:int):
        """Sets the limit someone can marry someone. 0 is unlimited."""
        if ctx.message.server.id not in self.settings:
            self.settings[ctx.message.server.id] = {}
        self.settings[ctx.message.server.id]['marry_limit'] = times
        self.save_settings()
        await self.bot.say("Done!")
       
    @commands.command(pass_context=True, no_pm=True)
    async def marrylimit(self, ctx):
        """Shows you the current marrylimit."""
        self.settings = dataIO.load_json("data/marry/settings.json")
        if (ctx.message.server.id not in self.settings) or ("marry_limit" not in self.settings[ctx.message.server.id]):
            await self.bot.say("There is no marry limit.")
        elif self.settings[ctx.message.server.id]['marry_limit'] == 0:
            await self.bot.say("There is no marry limit.")
        else:
            await self.bot.say("The marry limit is {}.".format(self.settings[ctx.message.server.id]['marry_limit']))
        
    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def massdivorce(self, ctx):
        """Divorces everyone on the server."""
        await self.bot.say("Are you sure you want to divorce everyone on the server? (yes/no)")
        answer = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
        if answer is None:
            await self.bot.say("K then not.")
            return
        elif "yes" in answer.content.lower():
            divorced = 0
            self.settings[ctx.message.server.id] = {'marry_limit': 1, 'disabled': False}
            self.save_settings()
            for role in ctx.message.server.roles:
                if " ❤ " in role.name:
                    try:
                        await self.bot.delete_role(role=role, server=ctx.message.server)
                        divorced = divorced + 1
                        self.settings[ctx.message.server.id] = {'marry_limit': 1, 'disabled': False}
                        self.save_settings()
                    except:
                        pass
            marchan = discord.utils.find(lambda c: c.name == 'marriage', ctx.message.server.channels)
            if marchan:
                await self.bot.say("Done! Divorced {} couples.".format(divorced))
                await self.bot.send_message(marchan, "{} divorced everyone ({} couples).".format(ctx.message.author.mention, divorced))
                self.settings[ctx.message.server.id] = {'marry_limit': 1, 'disabled': False}
                self.save_settings()
            else:
                try:
                    marchan = await self.bot.create_channel(ctx.message.server, "marriage")
                    await self.bot.say("Done! Divorced {} couples.".format(divorced))
                    await self.bot.send_message(marchan, "{} divorced everyone ({} couples).".format(ctx.message.author.mention, divorced))
                    self.settings[ctx.message.server.id] = {'marry_limit': 1, 'disabled': False}
                    self.save_settings()
                except:
                    await self.bot.say("Done! Everyone has been divorced. I suggest telling the server owner or moderators to make a #marriage channel though.")
                    return
        else:
            await self.bot.say("K then not.")
            return
            
    @commands.command(pass_context=True, no_pm=True)
    async def marrycount(self, ctx):
        """Counts all the married couples in this server."""
        count = 0
        for role in ctx.message.server.roles:
            if " ❤ " in role.name:
                count += 1
        if count == 1:
            await self.bot.say("There is currently {} married couple in this server.".format(count))
        else:
            await self.bot.say("There are currently {} married couples in this server.".format(count))
            
    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def admindivorce(self, ctx, person:discord.Member, lovedone:discord.Member):
        """Divorces someone by NAME. If the name is bigger than one word put quotes around it
        Example: "much name, such words"."""
        personx = person.id
        personx2 = lovedone.id
        times_married = self.settings[ctx.message.server.id][personx]
        times_married2 = self.settings[ctx.message.server.id][personx2]
        for role in ctx.message.server.roles:
            if person.name in role.name:
                if " ❤ " in role.name:
                    if lovedone.name in role.name:
                        try:
                            await self.bot.delete_role(ctx.message.server, role)
                            marchan = discord.utils.find(lambda c: c.name == 'marriage', ctx.message.server.channels)
                            if marchan:
                                await self.bot.send_message(marchan, "{} admindivorced {} and {}.".format(ctx.message.author.name, person.name, lovedone.name))
                                times_married = times_married - self.settings[ctx.message.server.id][personx]
                                times_married2 = times_married2 - self.settings[ctx.message.server.id][personx2]
                                self.settings[ctx.message.server.id][personx] = times_married
                                self.settings[ctx.message.server.id][personx2] = times_married2
                                self.save_settings()
                            else:
                                marchan = self.bot.create_channel(ctx.message.server, "marriage")
                                await self.bot.send_message(marchan, "{} admindivorced {} and {}.".format(ctx.message.author.name, person.name, lovedone.name))
                                times_married = times_married - self.settings[ctx.message.server.id][personx]
                                times_married2 = times_married2 - self.settings[ctx.message.server.id][personx2]
                                self.settings[ctx.message.server.id][personx] = times_married
                                self.settings[ctx.message.server.id][personx2] = times_married2
                                self.save_settings()
                            await self.bot.say("Succesfully divorced {} and {}.".format(person.name, lovedone.name))
                            return
                        except:
                            await self.bot.say("The role for the marriage was found but could not be deleted.")
                            return
        await self.bot.say("The role of that marriage could not be found.")
        
    @commands.command(pass_context=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def togglemarriage(self, ctx):
        """Toggles if members of your server should be able to marry each other using [p]marry."""
        if ctx.message.server.id not in self.settings:
            self.settings[ctx.message.server.id] = {'marrylimit': 0, 'disabled': False}
        if not self.settings[ctx.message.server.id]['disabled']:
            self.settings[ctx.message.server.id]['disabled'] = True
            await self.bot.say("Members can no longer marry each other anymore.")
        else:
            self.settings[ctx.message.server.id]['disabled'] = False
            await self.bot.say("Members can once again marry each other.")
        self.save_settings()


    def save_settings(self):
        dataIO.save_json("data/marry/settings.json", self.settings)
        
def check_folders():
    if not os.path.exists("data/marry"):
        print("Creating data/marry folder...")
        os.makedirs("data/marry")
    if not os.path.exists("data/marry/images"):
        print("Creating data/marry/images folder...")
        os.makedirs("data/marry/images")
        
def check_files():
    if not os.path.exists("data/marry/settings.json"):
        print("Creating data/marry/settings.json file...")
        dataIO.save_json("data/marry/settings.json", {})
        
def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Marry(bot))