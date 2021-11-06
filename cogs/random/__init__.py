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
        arr = split_message(message)
        response = f':point_right: {random.choice(arr)}'
        await ctx.send(response)

    @commands.command()
    async def shuffle(self, ctx, *, message: str):
        arr = split_message(message)
        random.shuffle(arr)
        
        arr = [f'**{index+1}.** {item}' for index, item in enumerate(arr)]

        response = '\n'.join(arr)
        await ctx.send(response)

def split_message(message):
    arr = re.split(',|\||\\n', message)
    arr = map(lambda s: s.strip(), arr)
    arr = filter(lambda s: len(s) > 0, arr)
    arr = list(arr)
    return arr

def setup(client):
    client.add_cog(Sample(client))
