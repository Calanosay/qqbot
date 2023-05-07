import nonebot
import requests
import re
import random
from nonebot import require
from nonebot.adapters.onebot.v11 import event
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
from .base import names


async def get_rating(tp, name):
    async with httpx.AsyncClient() as client:
        url = f"https://competitive-coding-api.herokuapp.com/api/{tp}/{name}"
        resp = await client.get(url)
        data = resp.json()

        if data["status"] != "Success":
            data = -1

    if data == -1:
        return -1
    return data["rating"]


# who = {"3191128724", "1143957699"}

search = on_regex("^(cf|at)查分")

@search.handle()
async def search_handler(bot: Bot, event: Event):
    name=str(event.get_message())[4:].strip().casefold().title()
    tp=str(event.get_message())[:2]
    if names.getname(name) != -1:
        name = names.getname(name)
    
    if tp == "at":
        tp = "atcoder"
    else: tp = "codeforces"
    rating=await get_rating(tp,name)
    if rating == "NA":
        rating = "0"
    if rating==-1:
        await search.finish("未找到该用户哦~")
    await search.finish(f"{name} 的 {tp} 分数是 {rating} 哦~")



