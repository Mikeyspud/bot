import sys
import discord
from discord.ext import commands

class Member(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded")

    @commands.command()
    async def claim(self, ctx, name: str):

        member = [member for member in self.client.outfit.members if member._id == ctx.author.id][0]
        if member.claimed():
            raise AlreadyClaimed
        else:
            member.claim(name=name)
            self.client.database.members.update_one({"_id": member._id}, {"$set": vars(member)})

    @commands.command()
    async def unclaim(self, ctx):

        member = [member for member in self.client.outfit.members if member._id == ctx.author.id][0]
        if not member.claimed():
            raise NotClaimed
        else:
            member.unclaim()
            self.client.database.members.update_one({"_id": member._id}, {"$set": vars(member)})

    @commands.command()
    async def award(self, ctx, member: discord.Member, xp):

        member = [member for member in self.client.outfit.members if member._id == member.id][0]
        member.award(xp)


class AlreadyClaimed(Exception):

    pass

class NotClaimed(Exception):

    pass

def setup(client):
    client.add_cog(Member(client))    