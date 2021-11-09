import discord
import random
from discord.ext import commands
from datetime import datetime
from utils import store

class GayPercent(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Gay command is ready")

    @commands.command(aliases=['gay%'], help='Đo độ cong của người dùng')
    async def howgay(self, ctx: commands.Context, *mentions: discord.Member):
        description = []
        board = store.get("board")
        if board == None:
            board = []

        for member in mentions:
            percent = randomPercent(member)
            description.append(f'**{member.display_name}** có {percent}% tỉ lệ gay')
            tuple_get = (f'{member.display_name}', percent)
            if (tuple_get in board):
                pass
            else:
                board.append(tuple_get)
            store.set("board", board)

        embed = discord.Embed(
            title="🏳️‍🌈 Bạn có thẳng như mình nghĩ?",
            description='\n'.join(description),
            color=discord.Color.orange(),
        )

        if len(description) == 0:
            percent = randomPercent(ctx.author)
            flag = '🏳️‍🌈' if percent > 25 else '🏳️'
            ctx.author = str(ctx.author)
            tuple_get = (f'{ctx.author[:ctx.author.find("#")]}', percent)
            if (tuple_get in board):
                pass
            else:
                board.append(tuple_get)
            store.set("board", board)
            await ctx.send(f'{flag} Bạn có {percent}% tỉ lệ gay')
        else:
            await ctx.send(embed=embed)

def randomPercent(seed):
    today = datetime.today().strftime('%Y-%m-%d')
    store.set("time",today)
    seed = f'{seed}/{today}'
    rng = random.Random(seed)
    return rng.randint(0, 100)

def setup(client):
    client.add_cog(GayPercent(client))
