import sys
import discord
from discord.ext import commands

class Squad(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded")

    @commands.command(
        brief="Allows management of squads"
    )
    async def squad(self, ctx, squad_name, *args):

        operation = self.client.get_operation(ctx=ctx)
        kwargs = self.client.parse_keyword_args(*args)
        try:
            squad = operation.squads[squad_name]
            self.client.prevent_dynamic_attributes(ctx, squad, **kwargs)
            [squad.__setattr__(key, value) for key, value in kwargs.items()]
        except KeyError:
            squad = operation.add_squad(name=squad_name, **kwargs)

    
    class SquadDoesntExist(Exception):

        pass


def setup(client):
    client.add_cog(Squad(client))    