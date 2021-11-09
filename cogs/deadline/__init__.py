import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils import store
import unicodedata
from cogs.deadline import deadline_bot
COMMAND_LIST = [
    ['deadline' , """
        >>deadline all : Tổng quan các key deadline hiện có
        >>deadline <key> : Xem trực quan tất cả deadline của <key>
        >>deadline <key> day : Xem trực quan tất cả deadline của <key> trong 24h
        >>deadline <key> week : Xem trực quan tất cả deadline của <key> trong 7 ngày
        >>deadline <key> month : Xem trực quan tất cả deadline của <key> trong tháng
        >>deadline <key> list : Xem tất cả deadline của <key> dưới dạng liệt kê đầy đủ
        >>deadline add <key> "title" "description" "time end" "date end" : thêm deadline mới
        Ví dụ: >>deadline add 21KDL "NMLT" "1000 bai code thieu nien" 12:30:01 21/21/2021
        >>deadline remove <key> <code> : xóa 1 deadline dựa trên <key> và <code>
        Lưu ý: code của 1 deadline có thể xem bằng ">>deadline <key> list"
        Ví dụ: >>deadline remove 21KDL 21KDL01
        >>deadline delete <key> : Xóa 1 <key>
    """]
]
class deadline(commands.Cog):

    def __init__(self, client: discord.Client):
        self.client = client

    # Khi lệnh được tạo ra thì sẽ chạy hàm này đầu tiên
    @commands.Cog.listener()
    async def on_ready(self):
        print("Deadline command is ready")
        pass

    # Định nghĩa lệnh "Deadline"
    @commands.command(help = 'quản lý deadline, gõ ">>deadline help" để xem các lệnh có sẵn')
    async def deadline(self, ctx, *args):
        if (args[0] == 'all'):
            embed= deadline_bot.display.all_deadline()
            await ctx.send(embed = embed)
        elif (args[0] == 'help'):
            embed = discord.Embed(
                title = 'deadline command help',
                description = f'{COMMAND_LIST[0][1]}',
                color = discord.Color.orange()
            )
            await ctx.send(embed=embed)
        elif (len(args) == 1):
            embed, file = deadline_bot.display.deadline_visualization(args[0])
            await ctx.send(embed = embed, file = file)
        elif (args[0] == 'add'):
            #try:
                if (len(args) == 7):
                    tmp = str(args[4])
                    if(len(tmp) <= 2):
                        tmp += ':00:00'
                    elif (len(tmp) <= 5):
                        tmp += ':00'
                    deadline_bot.action.add(args[1], args[2], args[3], tmp + ' ' + str(args[5]), args[6])
                elif (len(args) == 6):
                    tmp = str(args[4])
                    if(len(tmp) <= 2):
                        tmp += ':00:00'
                    elif (len(tmp) <= 5):
                        tmp += ':00'
                    deadline_bot.action.add(args[1], args[2], args[3], tmp + ' ' + str(args[5]))
                else:
                    deadline_bot.action.add(args[1], args[2], args[3], '00:00:00' + ' ' + str(args[4]))
                await ctx.send(f"`done! deadline {args[2]} added`")
            #except:
            #   await ctx.send("`error: can't add this deadline | error code: a1`")
        elif (args[0] == 'remove'):
            try:
                deadline_bot.action.delete(args[1], args[2])
                await ctx.send(f'`completed remove deadline code = {args[2]}`')
            except:
                await ctx.send(f"`can't remove deadline code = {args[2]}`")
        elif (args[0] == 'delete'):
            try:
                deadline_bot.action.delete_data(args[1])
                await ctx.send(f'`completed remove deadline key = {args[1]}`')
            except:
                await ctx.send(f"`can't remove deadline key = {args[1]}`")
        elif (args[1] == 'list'):
            embed = deadline_bot.display.deadline_list(args[0])
            await ctx.send(embed = embed)
        elif (args[1] == 'day'):
            embed, file = deadline_bot.display.deadline_visualization(args[0], 'day')
            await ctx.send(file = file, embed = embed)
        elif (args[1] == 'week'):
            embed, file = deadline_bot.display.deadline_visualization(args[0], 'week')
            await ctx.send(file = file, embed = embed)
        elif (args[1] == 'month'):
            embed, file = deadline_bot.display.deadline_visualization(args[0], 'month')
            await ctx.send(file = file, embed = embed)
        

def setup(client):
    client.add_cog(deadline(client))
