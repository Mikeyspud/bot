import discord
from discord.ext import commands


class Event(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded")

    @commands.command()
    async def create(self, ctx, name, start_time):

        event = self.client.constants.event()(_id=ctx.channel.id, name=name, start_time=start_time)
        self.client.outfit.add_event(event)
        await ctx.send(embed=event.embed())

    @commands.command()
    async def group(self, ctx, name):

        event = self.client.outfit.event(ctx.channel.id)
        print(event)
        await ctx.send(event)


def setup(client):
    client.add_cog(Event(client))
