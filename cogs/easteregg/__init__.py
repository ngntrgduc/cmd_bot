import os
import discord
from discord.ext import commands

class Suprise(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client
        self.store =[]

    @commands.Cog.listener()
    async def on_ready(self):
        #print("suprise is runnig")
        pass

    @commands.command(help="Store basic to prepare for a send message")
    async def get(self, ctx):
        attachment_url = ctx.message.attachments[0].url
        #file_request = requests.get(attachment_url)
        #print(attachment_url)
        self.store.append(attachment_url)

    @commands.command(pass_context = True,help="Send to channel a message which is getted")
    async def send_to(self,ctx,Id_channel:int,tag:discord.Member =None):
        channel = self.client.get_channel(int(Id_channel))
        if channel:
            await channel.send(f'{tag.mention}')
            if self.store != []:
                await channel.send(self.store[-1])

def setup(client):
    client.add_cog(Suprise(client))