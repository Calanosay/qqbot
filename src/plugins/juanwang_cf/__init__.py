# coding=utf-8
import asyncio
import time

import nonebot
import requests
import re
import random
from nonebot import require
from nonebot.adapters.onebot.v11 import event
from .base import *
import json
import httpx
from nonebot import on_command, on_message, on_regex, export
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent, Event, PrivateMessageEvent
from nonebot.adapters.onebot.v11.utils import unescape
from nonebot.params import State
from nonebot.rule import to_me
import threading

scheduler = require("nonebot_plugin_apscheduler").scheduler


async def get_last_problem(name):
    data = -1
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    async with httpx.AsyncClient(timeout=None, headers=headers) as client:
        url = f"https://codeforces.com/api/user.status?handle={name}&page=1"
        resp = await client.get(url)
        try:
            data = resp.json()
        except:
            print("有内鬼!" + name)
            print(resp.text)

        if data == -1 or data["status"] != "OK" or len(data["result"]) == 0:
            data = -1
    if data == -1:
        return -1
    return data["result"][0]


# who = {"3191128724", "1143957699"}

juanwang = on_regex("^看(cf|CF|cF|Cf)卷王")
bukanle = on_regex("^停看(cf|CF|cF|Cf)卷王")
showout = on_regex("^当前(cf|CF|cF|Cf)卷王$")


@juanwang.handle()
async def juanwang_handler1(bot: Bot, event: PrivateMessageEvent):
    await juanwang.finish("抱歉,当前仅支持群聊看卷王哦~")


@juanwang.handle()
async def juanwang_handler2(bot: Bot, event: GroupMessageEvent):
    name = str(event.get_message())[5:].strip()
    if len(name) == 0:
        await juanwang.finish("请说明要看哪位卷王哦~")
    s = re.search('[\w|\x80-\xff]*', name).group()
    if name != s:
        await juanwang.finish("请不要输入奇怪的字符哦~")
    newname = name.casefold().title()
    if names.getname(newname) != -1:
        newname = names.getname(newname)
    # if user in who:
    #     await juanwang.finish("抱歉,您一个人都不能看~")

    # if newname == "Calanosay" or name == "434015":
    #     await juanwang.finish("抱歉，这位卷王由于特殊原因，不能看")
    if newname in Juanwangs.getall():
        await juanwang.finish("这位卷王已经被人盯上了哦,你不能再看他了(可能是其他群聊的人喔)")
    last = await get_last_problem(newname)
    if last == -1:
        await juanwang.finish("未查到该卷王或该卷王无提交记录~")
    if "contestId" not in last:
        await juanwang.finish("该卷王由于上次做的题目非常规题目，暂无法查看。")
    contest = last["contestId"]
    problem = last['problem']['index']
    now = "CF" + str(contest) + problem
    Juanwangs.setlast(newname, now)
    Juanwangs.setlastvp(newname, "qefqef")
    Juanwangs.addpeople(newname)
    tp = last['author']["participantType"]
    if tp == "VIRTUAL" or tp == "CONTESTANT":
        Juanwangs.setlastvp(newname, contest)
    # doing.add(newname)
    Juanwangs.setGroup(newname, event.group_id)
    await juanwang.send(f"现在开始持续关注CF卷王{newname}啦！如果想停止,请说停看卷王某某某~")

cnt = 0
async def crawl(user):
    global cnt
    cnt += 1
    await asyncio.sleep(cnt * 1)
    if cnt == len(Juanwangs.getall()):
        cnt = 0
    st = time.time()    
    now = await get_last_problem(user)
    ed = time.time()
    print("现在正在执行:" + user + "的CF任务，耗时" + str(ed - st))
    if now == -1:
        return
    if "contestId" not in now:
        return
    tp = now['author']["participantType"]
    contest = now["contestId"]

    if tp == "VIRTUAL" or tp == "CONTESTANT":
        if contest != Juanwangs.getlastvp(user):
            Juanwangs.setlastvp(user, contest)
            flag = "VP"
            if tp == "CONTESTANT":
                flag = "打CF比赛"
            await nonebot.get_bot().send_group_msg(message=Message(f"卷王{user}又开始{flag}了！他参赛的场次编号为 {contest}"),
                                                   group_id=int(Juanwangs.getGroup(user)))
    elif tp == "PRACTICE":
        problem = now['problem']['index']
        now = "CF" + str(contest) + problem
        if now != Juanwangs.getlast(user):
            Juanwangs.setlast(user, now)
            await nonebot.get_bot().send_group_msg(message=Message(f"卷王{user}又开始做题了！他现在在做{now}"),
                                                   group_id=int(Juanwangs.getGroup(user)))


@scheduler.scheduled_job('interval', minutes=3, max_instances=200)
async def handler():
    await asyncio.gather(*(crawl(x) for x in Juanwangs.getall()))


@bukanle.handle()
async def bukanle_handler(bot: Bot, event: Event):
    name = str(event.get_message())[6:].strip().casefold().title()
    if names.getname(name) != -1:
        name = names.getname(name)
    # if event.get_user_id() not in bot.config.superusers:
    #     await bukanle.finish("只有超管才能指挥我~")
    if name.casefold().title() not in Juanwangs.getall():
        await bukanle.finish("没人在看这位卷王哦~")
    Juanwangs.delpeople(name)
    if name == "Artemis_Bow":
        await bot.call_api(api="send_group_msg", message="gaygay偷偷取消卷王监视啦！！！", group_id="1061040394")
        await bot.call_api(api="send_group_msg", message="gaygay偷偷取消卷王监视啦！！！", group_id="1061040394")
        await bot.call_api(api="send_group_msg", message="gaygay偷偷取消卷王监视啦！！！", group_id="1061040394")
    await bukanle.finish(f"好的，我已经没有在看CF卷王{name}啦！")


@showout.handle()
async def showout_handler(bot: Bot, event: GroupMessageEvent):
    List = []
    for i in Juanwangs.getall():
        if Juanwangs.getGroup(i) == event.group_id:
            List.append(i)
    if len(List) == 0:
        await showout.finish("当前本群CF还没有卷王哦~")
    text = f"现在本群CF卷王有{len(List)}位："
    idx = 0
    for i in List:
        idx += 1
        text = text + f"\n{idx}:{i}"
        if idx == 10:
            text = text + "\n......"
            break
    await showout.finish(text)
