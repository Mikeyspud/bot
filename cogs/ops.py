import sys
import discord
from discord.ext import commands

class Ops(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} loaded")

    @commands.command(
        brief="Creates an operation"
    )
    async def ops(self, ctx, *args):

        operation = self.client.get_operation(ctx)
        kwargs = self.client.parse_keyword_args(*args)

        if operation:
            self.client.prevent_dynamic_attributes(ctx, operation, **kwargs)
            [operation.__setattr__(key, value) for key, value in kwargs.items()]    
        else:
            operation = self.client.Ops(_id=ctx.channel.id, **kwargs)
            self.client.ops_list[ctx.channel.id] = operation
    
    class MissingName(Exception):

        pass

    class OperationDoesntExist(Exception):

        pass

    class DynamicAttributeCreation(Exception):

        pass

def setup(client):
    client.add_cog(Ops(client))    