import sys
import discord
from discord.ext import commands

class Member(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.database = self.client.Member.database

    def get_member(self, member: discord.Member):

        return self.client.Member.load(member=member)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded")

    @commands.command(
        brief="Inspects a players information", 
        description="Queries the database to grab the properties of an outfit member. Optional argument taken as a mention"
    )
    async def inspect(self, ctx: commands.Context, member: discord.Member = None):

        if member is None:
            member = self.get_member(member=ctx.author)
        else:
            member = self.get_member(member=member)
        await ctx.send(embed=member.embed())

    @commands.command(
        brief="Claims a Planetside 2 Character in the outfit",
        description="Claims a Planetside 2 Character in the outfit. Argument is your characters username"
    )
    async def claim(self, ctx: commands.Context, ps2_name: str):

        ps2_id = self.client.Member.get_member_id_by_name(name=ps2_name)
        if ps2_id not in self.client.outfit.members:
            raise InvalidCharacter

        member = self.get_member(member=ctx.author)
        member.claim(ps2_name=ps2_name)
        member.save(database=self.database)

    @commands.command(
        brief="Will unclaim any character you have claimed",
        description="Unclaims a planetside 2 character you have claimed. No arguments"
    )
    async def unclaim(self, ctx):

        member = self.get_member(member=ctx.author)
        member.unclaim()
        member.save(database=self.database)

    @commands.command(
        brief="Will award a character with points",
        description="Awards a character with points. User argument is mention, amount argument is an integer (positive or negative)"
    )
    async def award(self, ctx, user: discord.User, amount: int):

        member = self.get_member(member=ctx.author)
        member.award(points=amount)
        member.save(database=self.database)

class AlreadyClaimed(Exception):

    pass

class InvalidCharacter(Exception):

    pass


def setup(client):
    client.add_cog(Member(client))    