import os
import discord
from discord.ext import commands

class Suprise(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client
        self.mess =[]

    @commands.Cog.listener()
    async def on_ready(self):
        #print("suprise is runnig")
        pass

    @commands.command(help="Store basic to prepare for a send message include txt/pic or bold ")
    async def get(self, ctx ,*,message = ""):
        #setting embed
        self.embed = discord.Embed(
            title="Đây là Message từ ai đó?",
            description=''.join(message),
            color=discord.Color.blue(),
        )
        #setting/check if have a picture where send
        try:
            attachment_url = ctx.message.attachments[0].url
            self.embed.set_image(url=attachment_url)
        except IndexError:
            pass
        await ctx.send("Getted!")
        #prepare for send
        self.mess.append(self.embed)

    @commands.command(pass_context = True,help="Send to channel(id) a message which is getted include tag/tags or not")
    async def send_to(self,ctx,Id_channel:int,*tags:discord.Member):
        #send a embeg(message in getted) to Id_channel have(or not) tags person
        channel = self.client.get_channel(int(Id_channel))
        if channel:
            if len(tags) != 0:
                await channel.send(" ".join([tag.mention for tag in tags]))
        await channel.send(embed=self.embed)

def setup(client):
    client.add_cog(Suprise(client))