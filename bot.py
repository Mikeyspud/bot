import os
import sys
import discord
import pymongo
from ops import Ops
from member import Member
from outfit import Outfit
from database import Database
from constants import Constants
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

class Bot(commands.Bot):

    def __init__(self, outfit_name: str, guild_id: int, member_role_id: int, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.guild_id = guild_id
        self.member_role_id = member_role_id
        self.outfit = Outfit(name=outfit_name)
        self.database = Database(tag=self.outfit.alias)()
        self.Member = Member(database=self.database.members)
        self.Ops = Ops
        self.ops_list = dict()
        self.add_commands()

    @property
    def guild(self) -> discord.Guild:

        return self.get_guild(id=self.guild_id)

    @property
    def member_role(self) -> discord.Role:

        return self.guild.get_role(role_id=self.member_role_id)

    def add_operation(self, operation):

        if operation._id in self.ops_list:
            raise self.OperationExists
        else:
            self.ops_list[operation._id] = operation

    async def on_ready(self):

        def _parse_discord_member_ids():

            for member in [member for member in self.guild.members if self.member_role in member.roles]:
                self.Member.create(member=member)

        print(f"{self.__class__.__name__} loaded")
        _parse_discord_member_ids()

    async def on_command_error(self, ctx, error, *args, **kwargs):

        error_embed = self.error_embed()
        error_embed.add_field(name="Error", value=error)
        await ctx.send(embed=error_embed)
        raise error

    def error_embed(self):

        embed = discord.Embed(
            title="BJay Signup Bot",
            description="Debug Message",
            color=0xebc20a
        )
        embed.set_author(
            name=f"[{self.outfit.alias}] {self.outfit.name}",
            icon_url=Constants.outfit_icon()
        )
        embed.set_footer(text="Message \"[BJay] 3rdPartyAimAssist\" if you think this errors shouldnt happen")

        return embed

    def prevent_dynamic_attributes(self, ctx, obj, **kwargs):

        for attribute in kwargs:
            try:
                obj.__getattribute__(attribute)
            except AttributeError:
                raise self.DynamicAttributeCreation

    def get_operation(self, ctx):

        try:
            return self.ops_list[ctx.channel.id]
        except KeyError:
            return None

    def add_commands(self):

        @self.command(
            brief="No Touchy!",
            description="I said NO TOUCHY!"
        )
        async def load(ctx, extension):
            self.load_extension(f"cogs.{extension}")

        @self.command(
            brief="No Touchy!",
            description="I said NO TOUCHY!"
        )
        async def unload(ctx, extension):
            self.unload_extension(f"cogs.{extension}")

        for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                self.load_extension(f"cogs.{f[:-3]}")

    def parse_keyword_args(self, *args) -> dict:

        if len(args) % 2 != 0:
            raise self.InvalidKeywordArgs

        arguments = dict()
        for i in range(0, len(args), 2):
            arguments[args[i]] = args[i+1]

        return arguments

    class InvalidKeywordArgs(Exception):

        pass

    class OperationExists(Exception):

        pass

    class DynamicAttributeCreation(Exception):

        pass
        

if __name__ == "__main__":

    token = "not my token"
    bot = Bot(command_prefix="!", outfit_name="Get Off My Base Peasants", guild_id=406492955629715456, member_role_id=722106886069157888, intents=intents)
    bot.run(token)