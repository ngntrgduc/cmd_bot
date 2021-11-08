import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import store

load_dotenv()
Var_Channel = os.getenv("VAR_CHANNEL_ID")
Cfs_Channel = os.getenv("CFS_CHANNEL_ID")
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')

class Cfs(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client
        self.mess =[]

    @commands.Cog.listener()
    async def on_ready(self):
        #print("suprise is runnig")
        pass

    @commands.command(help="viết bất kỳ thứ gì (đính kèm ảnh hoặc không)",pass_context=True)
    async def cfs(self,ctx,*,message="",):
        self.embed = discord.Embed(
            title="Đây là Confession từ ai đó với ngàn yêu thương ?",
            description=''.join(message),
            color=discord.Color.blue(),
        )
        # setting/check if have a picture where send
        try:
            attachment_url = ctx.message.attachments[0].url
            self.embed.set_image(url=attachment_url)
        except IndexError:
            pass
        await ctx.send("```Getted!```")
        # prepare for send
        self.mess.append(self.embed)

        #send a message to reaction
        self.var_channel = self.client.get_channel(int(Var_Channel))
        if self.var_channel:
            """if len(tags) != 0:
                await channel.send(" ".join([tag.mention for tag in tags]))"""
            self.msg = await self.var_channel.send(embed=self.embed)
            await self.msg.add_reaction("✅") # V is accpect
            await self.msg.add_reaction("❌") # X is not
            await self.msg.add_reaction("❔") # ? is waiting

    # waiting util reaction and send back to cfs channel
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        cfs_channel = self.client.get_channel(int(Cfs_Channel))
        if (str(reaction.emoji) == '✅') and (user != self.client.user):
            await self.var_channel.send(f"```Accepted by {user}```")
            await cfs_channel.send(embed=self.embed)
        elif (str(reaction.emoji) == '❌') and (user != self.client.user):
            await self.var_channel.send(f"```No Accepted by {user}```")
        elif (str(reaction.emoji) == '❔') and (user != self.client.user):
            await self.var_channel.send(f"```{user} cant process this Trường hợp```")
        else:
            pass

        # back_up not fisnish yet
        if (back_up := store.get("author")) == None:
            back_up = []
        back_up.append(str(sub(str(user.id))))
        store.set("author", back_up)


def setup(client):
    client.add_cog(Cfs(client))

def sub(input):
   #i will push a decrypt Khoa cant solve :>
    return input[::-1]