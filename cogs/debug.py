import sys
import discord
from discord.ext import commands

class Debug(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded")

    @commands.command(
        brief="Used to debug obviously"
    )
    async def debug(self, ctx):

        for operation in self.client.ops_list.values():
            await ctx.send(f"`{vars(operation)}`")
            for squad in operation.squads.values():
                await ctx.send(f"`{vars(squad)}`")

    

def setup(client):
    client.add_cog(Debug(client))    