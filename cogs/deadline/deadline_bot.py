'''
    @author : Nghi Gia
    this is an open-source project so everyone can read, edit and use this code for another program

    == love u my crushhhhh :3 ==
'''

import os
from typing import AsyncIterator
from utils import store
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import discord
import datetime
import regex
from dotenv import load_dotenv

store.load()
TIME_ZONE = os.getenv('TIME_ZONE')

class action():

    def __init__(self):
        pass

    # ====== create new deadline carledar ======

    def add(key, title, content, date, remind = 0):
        '''
            Hàm này dùng để thêm deadline mới vào store (remind mặc định là 0 maybe sẽ có update trong tương lai)
            Định dạng của code: key + 0 + cnt
        '''
        raw_data = store.get("deadline")
        if (raw_data == None):
            raw_data = {"_test_place" : []}
        if (key in raw_data):
            raw_data[key]["title"].append(title)
            raw_data[key]["content"].append(content)
            raw_data[key]["date"].append(date)
            raw_data[key]["remind"].append(remind)
            raw_data[key]["code"].append(f'{key}0{raw_data[key]["cnt"]}')
            raw_data[key]["cnt"] = raw_data[key]["cnt"] + 1
        else:
            tmp = {"title" : [], "content" : [], "date" : [], "remind" : [], "code" : [],"cnt" : 0}
            raw_data[key] = tmp
            raw_data[key]["title"].append(title)
            raw_data[key]["content"].append(content)
            raw_data[key]["date"].append(date)
            raw_data[key]["remind"].append(remind)
            raw_data[key]["code"].append(f'{key}0{raw_data[key]["cnt"]}')
            raw_data[key]["cnt"] = raw_data[key]["cnt"] + 1
        store.set("deadline", raw_data)

    def delete(key, code):
        '''
            Hàm này dùng để xóa deadline trong store dựa theo key và code
        '''
        raw_data = store.get("deadline")
        data = raw_data[key]
        try:
            idx = data["code"].index(code)
            data["title"].pop(idx)
            data["content"].pop(idx)
            data["date"].pop(idx)
            data["remind"].pop(idx)
            data["code"].pop(idx)
            raw_data[key] = data
            store.set("deadline", raw_data)
        except:
            print(f'error in deadline delete key = {key} | code = {code}')

    def get_data(key):
        '''
            Hàm này làm cho zui chứ không sử dụng tới =))
        '''
        raw_data = store.get("deadline")
        data = raw_data[key]
        return data

    def checker(key):
        '''
            Hàm này sẽ check deadline quá hạn theo key
            time_delta là mảng chứa thời gian còn lại của deadline theo ngày, nếu time_delta[i] <= 0 thì sẽ xóa đi
            Do việc xóa đi có thể gây lỗi lên toàn bộ data không bị xóa sẽ được lưu vào new_data, các data bị xóa sẽ bỏ qua
        '''
        raw_data = store.get("deadline")
        data = raw_data[key]
        new_data = {"title" : [], "content" : [], "date" : [], "remind" : [], "code" : [],"cnt" : 0}
        new_data["cnt"] = data["cnt"]
        now = datetime.datetime.utcnow() + datetime.timedelta(hours = int(TIME_ZONE))
        title = data['title']
        time_delta = [(datetime.datetime.strptime(time, '%H:%M:%S %d/%m/%Y') - now).total_seconds()/(60*60*24) for time in data['date']]
        for i in range(len(time_delta)):
            if (time_delta[i] > 0):
                new_data["title"].append(data["title"][i])
                new_data["content"].append(data["content"][i])
                new_data["date"].append(data["date"][i])
                new_data["remind"].append(data["remind"][i])
                new_data["code"].append(data["code"][i])
        raw_data[key] = new_data
        store.set("deadline", raw_data)

    def update_data():
        '''
            Hàm này sẽ check tất cả deadline quá hạn, được gọi trong hàm all_deadline và chỉ hoạt động nếu _time_delta so với lần cập nhật gần nhất >= 6 (6 tiếng)
            time_delta là mảng chứa thời gian còn lại của deadline theo ngày, nếu time_delta[i] <= 0 thì sẽ xóa đi
            Do việc xóa đi có thể gây lỗi lên toàn bộ data không bị xóa sẽ được lưu vào new_data, các data bị xóa sẽ bỏ qua
        '''
        raw_data = store.get('deadline')
        time_data = raw_data['last_update']
        last_update = datetime.datetime.strptime(time_data, '%H:%M:%S %d/%m/%Y')
        now = datetime.datetime.utcnow() + datetime.timedelta(hours = int(TIME_ZONE))
        _time_delta = (now - last_update).total_seconds()/(60*60)
        if (_time_delta >= 6):
            for key in raw_data.keys():
                if (key == '_test_place' or key == 'last_update'):
                    continue
                data = raw_data[key]
                new_data = {"title" : [], "content" : [], "date" : [], "remind" : [], "code" : [],"cnt" : 0}
                new_data["cnt"] = data["cnt"]
                time_delta = [(datetime.datetime.strptime(time, '%H:%M:%S %d/%m/%Y') - now).total_seconds()/(60*60*24) for time in data['date']]
                for i in range(len(time_delta)):
                    if (time_delta[i] > 0):
                        new_data["title"].append(data["title"][i])
                        new_data["content"].append(data["content"][i])
                        new_data["date"].append(data["date"][i])
                        new_data["remind"].append(data["remind"][i])
                        new_data["code"].append(data["code"][i])
                raw_data[key] = new_data
            st = str((datetime.datetime.utcnow() + datetime.timedelta(hours = int(TIME_ZONE))).strftime('%H:%M:%S %d/%m/%Y'))
            raw_data['last_update'] = st
            store.set("deadline", raw_data)

    def delete_data(key):
        '''
            Hàm này dùng để xóa key trong store
        '''
        raw_data = raw_data = store.get('deadline')
        try:
            del raw_data[key]
        except:
            pass
        store.set("deadline", raw_data)

class display():

    def __init__(self):
        pass

    def all_deadline():
        '''
            Hàm này sẽ trả về tất cả deadline hiện tại
            Đầu tiên sẽ gọi update_data để kiểm tra data đã được cập nhật trong khoảng thời gian < 6 tiếng chưa
            sau đó sẽ return 1 embed mô tả tổng quát về tất cả deadline
        '''
        action.update_data()
        raw_data = store.get("deadline")
        number_of_deadline = len(raw_data) - 2
        embed = discord.Embed(
            title = '📅 All deadlines is active',
            description = f'There ' + (' is ' if number_of_deadline == 1 else ' are ') + f'{number_of_deadline}' + (' deadline ' if number_of_deadline <= 1 else ' deadlines ') + 'is active now!',
            color = discord.Color.red()
        )
        for key in raw_data.keys():
            if (key == '_test_place' or key == 'last_update'):
                continue
            tmp = raw_data[key]["title"]
            embed.add_field(
                name = key,
                value = f'{len(tmp)}' + (' deadline ' if len(tmp) <= 1 else ' deadlines ') + 'is actived',
                inline=False
            )
        return embed

    def deadline_list(key):
        '''
            Hàm này trả về deadline của key theo dạng list
        '''
        action.checker(key) # Check data trong list đã được cập nhật chưa
        raw_data = store.get("deadline")
        data = raw_data[key]
        embed = discord.Embed(
            title = f'📅 {key} deadlines is ative now!',
            description = f'server time: {datetime.datetime.now()}',
            color = discord.Color.red()
        )
        for i in range(len(data["title"])):
            embed.add_field(
                name = f'{data["title"][i]}',
                value = f'''
                ```{data["date"][i]} | {data["code"][i]} | {data["remind"][i]}```
                {data["content"][i]}
                ''',
                inline=False
            )
        return embed

    def deadline_visualization(key, type = 'all'):
        '''
            Trực quan hóa deadline trong list sử dụng matplotlib và seaborn
        '''
        action.checker(key) # Check data trong list đã được cập nhật chưa
        raw_data = store.get("deadline")
        data = raw_data[key]
        now = datetime.datetime.utcnow() + datetime.timedelta(hours = int(TIME_ZONE))
        title = data['title']
        time_delta = [(datetime.datetime.strptime(time, '%H:%M:%S %d/%m/%Y') - now).total_seconds()/(60*60*24) for time in data['date']]
        max_time_delta = 1000000007
        if (type == 'day'):
            max_time_delta = 1
        elif (type == 'week'):
            max_time_delta = 7
        elif (type == 'month'):
            max_time_delta = 30

        plot_title = []
        plot_time_delta = []
        for i in range(len(title)):
            if (time_delta[i] <= max_time_delta):
                plot_title.append(title[i])
                plot_time_delta.append(time_delta[i])

        try:
            fig, axes = plt.subplots()
            plt.style.use('ggplot')
            ax = sns.barplot(y = plot_title, x = plot_time_delta);
            ax.set_xlabel('time remaining(days)')
            ax.set_ylabel('')
            ax.set_title(('Deadline' if len(title) == 1 else 'Deadlines') + f' remaining of {key}')
            fig.savefig(f'deadline_{key}_all.png')
            embed = discord.Embed(
                title = f'All ' + ('deadline' if len(title) == 1 else 'deadlines') + f' of ' f'{key}',
                description = f'server time: {now}',
                color = discord.Color.red()
            )
            file = discord.File(f'deadline_{key}_all.png' ,filename="f'deadline_{key}_all.png")
            embed.set_image(url="attachment://f'deadline_{key}_all.png")
            return embed, file
        except:
            embed = discord.Embed(
                title = 'There are no deadline is activated now or a error has been raised!',
                description = f'server time: {now}',
                color = discord.Color.red()
            )
            file = discord.File(f'assets/error.jpg' ,filename="assets/error.jpg")
            return embed, file

if __name__ == '__main__':
    raw_data = store.get("deadline")
    st = str((datetime.datetime.utcnow() + datetime.timedelta(hours = int(TIME_ZONE))).strftime('%H:%M:%S %d/%m/%Y'))
    raw_data['last_update'] = st
    store.set("deadline", raw_data)
