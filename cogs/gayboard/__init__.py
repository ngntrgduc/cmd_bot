import os
import discord
from discord.ext import commands
from datetime import datetime
import store


class gayboard(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client

    # Khi lệnh được tạo ra thì sẽ chạy hàm này đầu tiên
    @commands.Cog.listener()
    async def on_ready(self):
        today = datetime.today().strftime('%Y-%m-%d')
        yesterday = store.get("time")
        if today >= yesterday:
            store.delete("board")
            store.set("board", [])
        print("gayboard is running")

    @commands.command(help='Bảng xếp hạng độ gay trong ngày')
    async def gayboard(self,ctx:commands.Context):
        board = store.get("board")
        board = sorted(board, key=lambda x: x[1] ,reverse=True)
        out = []
        for i in range(0, len(board)):
            out.append(f'{i+1} : {board[i][0]} có tỉ lệ gay {board[i][1]}%')

        embed = discord.Embed(
            title="🏳️‍🌈 Bạn nghĩ bạn gay ư?",
            description='\n'.join(out),
            color=discord.Color.blue(),
        )

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(gayboard(client))