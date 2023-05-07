import nonebot
import requests
import re
import random
import httpx
from nonebot import on_command, on_message, on_regex, export
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent, Event,PrivateMessageEvent
from nonebot.adapters.onebot.v11.utils import unescape
from nonebot.params import State
from nonebot.rule import to_me
from .base import *
from nonebot import require

scheduler = require("nonebot_plugin_apscheduler").scheduler


async def get_last_problem(name):
    url = f"https://www.luogu.com.cn/record/list?pid=&language=&orderBy=0&user={name}&page=1"

    key = {
        "__client_id": "f338556c062991022a460938c417f8513a7655f7",
        "_uid": "434015",
        "login_referer": "https%3A%2F%2Fwww.luogu.com.cn%2F"
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    async with httpx.AsyncClient(timeout=None) as client:
        data = await client.get(url, cookies=key, headers=headers)
        res = re.finditer(r'pid%22%3A%22(?P<t1>.*?)%22', str(data.content))
        flag = False
        for i in res:
            flag = True
            ans = i.group("t1")
            break
        if not flag:
            ans = ''
    return ans


# who = {"3191128724", "1143957699"}
juanwang = on_regex("^看卷王")
bukanle = on_regex("^停看卷王")
showout = on_regex("^当前卷王$")


@juanwang.handle()
async def juanwang_handler1(bot: Bot, event: PrivateMessageEvent):
    await juanwang.finish("抱歉,当前仅支持群聊看卷王哦~")


@juanwang.handle()
async def juanwang_handler2(bot: Bot, event: GroupMessageEvent):
    name = str(event.get_message())[3:].strip()
    s = re.search('[\w|\x80-\xff]*', name).group()
    if name != s:
        await juanwang.finish("请不要输入奇怪的字符哦~")
    newname = name.casefold().title()
    user = str(event.get_user_id())
    # if user in who:
    #     await juanwang.finish("抱歉,您一个人都不能看~")

    if len(name) == 0:
        await juanwang.finish("请说明要看哪位卷王哦~")
    # if name == "Calanosay" or name == "434015":
    #     await juanwang.finish("抱歉，这位卷王由于特殊原因，不能看")
    if names.getname(newname) != -1:
        newname = names.getname(newname)
    if newname in Juanwangs.getall():
        await juanwang.finish("这位卷王已经被人盯上了哦,你不能再看他了(可能是其他群聊的人喔)")
    last = await get_last_problem(newname)
    if len(last) == 0:
        await juanwang.finish("未查到该卷王或这位卷王已限制了搜索权限~")
    Juanwangs.setlast(newname, last)
    Juanwangs.addpeople(newname)
    Juanwangs.setGroup(newname, event.group_id)
    await juanwang.send(f"现在开始持续关注洛谷卷王{newname}啦！如果想停止,请说停看卷王某某某")


@scheduler.scheduled_job('interval', minutes=1,max_instances=61)
async def handler():
    for user in Juanwangs.getall():
        now = await get_last_problem(user)
        print("现在正在执行:" + user + "的洛谷任务，题目为" + now)
        if len(now) == 0:
            continue
        if now[:2] == "CF":
            continue
        if now != Juanwangs.getlast(user):
            Juanwangs.setlast(user, now)
            await nonebot.get_bot().send_group_msg(message=Message(f"卷王{user}又开始做题了！他现在在做{now}"),
                                                   group_id=int(Juanwangs.getGroup(user)))


@bukanle.handle()
async def bukanle_handler(bot: Bot, event: Event):
    name = str(event.get_message())[4:].strip().casefold().title()
    if names.getname(name) != -1:
        name = names.getname(name)
    # if event.get_user_id() not in bot.config.superusers:
    #     await bukanle.finish("只有超管才能指挥我~")
    if name.casefold().title() not in Juanwangs.getall():
        await bukanle.finish("没人在看这位卷王哦~")
    Juanwangs.delpeople(name)
    await bukanle.finish(f"好的，我已经没有在看洛谷卷王{name}啦！")


@showout.handle()
async def showout_handler(bot: Bot, event: Event):
    List=[]
    for i in Juanwangs.getall():
        if Juanwangs.getGroup(i) == event.group_id:
            List.append(i)
    if len(List) == 0:
        await showout.finish("现在本群还没有洛谷卷王哦~")
    text = f"当前本群洛谷卷王有{len(List)}位："
    idx = 0
    for i in List:
        idx += 1
        text = text + f"\n{idx}:{i}"
        if idx == 10:
            text = text + f"\n......"
            break
    await showout.finish(text)
