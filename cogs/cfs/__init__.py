import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import store
from datetime import datetime

load_dotenv()
Var_Channel = os.getenv("VAR_CHANNEL_ID")
Cfs_Channel = os.getenv("CFS_CHANNEL_ID")

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
            color= 0x1aeb5f,
            timestamp = datetime.utcnow()
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
            self.accept =await self.msg.add_reaction("✅") # V is accpect
            await self.msg.add_reaction("❌") # X is not
            await self.msg.add_reaction("❔") # ? is waiting

        # back_up not fisnish yet
        back_up = store.get("author")
        if back_up == None:
            back_up = []
        back_up.append(str(sub(str(ctx.author.id))))
        store.set("author", back_up)


    # waiting util reaction and send back to cfs channel
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        channel = self.client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = self.client.get_user(payload.user_id)
        if not user:
            user = await self.client.fetch_user(payload.user_id)
        # instead of reaction we should use payload.emoji
        # for example:
        cfs_channel = self.client.get_channel(int(Cfs_Channel))
        now  = datetime.now()
        current_time  = now.strftime("%H:%M:%S")
        if (str(payload.emoji) == '✅') and (user != self.client.user) and (payload.channel_id != int(Cfs_Channel)) :
            await self.var_channel.send(f"```Cfs at  {current_time}  was Accepted by {user}```")
            await self.msg.delete()
            self.msg = await cfs_channel.send(embed=self.embed)
            # await self.msg.clear_reaction("✅") sau là clear reaction
        elif (str(payload.emoji) == '❌') and (user != self.client.user) and (payload.channel_id != int(Cfs_Channel)):
            await self.var_channel.send(f"```Cfs at  {current_time} No Accepted by {user}```")
        elif (str(payload.emoji) == '❔') and (user != self.client.user) and (payload.channel_id != int(Cfs_Channel)):
            await self.var_channel.send(f"```{user} cant process this Trường hợp```")
        else:
            pass


def setup(client):
    client.add_cog(Cfs(client))

def sub(input):
   #i will push a decrypt Khoa cant solve :>
    return input[::-1]