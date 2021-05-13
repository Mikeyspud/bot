import os
import sys
import discord
import pymongo.errors
from member import Member
from outfit import Outfit
from database import Database
from constants import Constants
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

class Bot(commands.Bot):

    def __init__(self, outfit_name: str, *args, **kwargs):

        self.outfit = Outfit(name=outfit_name)
        self.database = Database().bjay
        self.constants = Constants
        super().__init__(*args, **kwargs)
        self.add_commands()

    async def on_ready(self):

        self.guild = self.get_guild([guild.id for guild in self.guilds if guild.id == 825061737811410985][0])
        self.get_outfit_members()
        print(f"{self.__class__.__name__} loaded")

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

    def add_commands(self):

        @self.command()
        async def load(ctx, extension):
            self.load_extension(f"cogs.{extension}")

        @self.command()
        async def unload(ctx, extension):
            self.unload_extension(f"cogs.{extension}")

        for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                self.load_extension(f"cogs.{f[:-3]}")

    def get_outfit_members(self):

        members = [Member(_id=member.id) for member in self.guild.members if self.guild.get_role(Constants.member_identifier()) in member.roles]
        [self.outfit.add_member(member) for member in members]

if __name__ == "__main__":

    token = "NzkzMjEyNDUzMjg2MTgyOTIy.X-o-qg.XoTvwbPC-SOVrBMR6nHNiUz8fg8"
    bot = Bot(command_prefix="#", outfit_name="Get Off My Base Peasants", intents=intents)
    bot.run(token)