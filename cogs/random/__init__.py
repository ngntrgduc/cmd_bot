import re
import random
import discord
from discord.ext import commands

class Sample(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Random command is ready')

    @commands.command(aliases=['choose'])
    async def pick(self, ctx, *, message: str):
        arr = map(lambda s: s.strip(), re.split(',|\|', message))
        arr = filter(lambda s: len(s) > 0, arr)
        arr = list(arr)

        response = f':point_right: {random.choice(arr)}'
        await ctx.send(response)

def setup(client):
    client.add_cog(Sample(client))
