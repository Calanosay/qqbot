import asyncio

import nonebot
from nonebot import on_message,on_request,on_regex
from nonebot.adapters.onebot.v11 import PRIVATE_FRIEND,Bot, Event, MessageEvent,FriendRequestEvent,GroupMessageEvent,GroupRequestEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import export
from nonebot.rule import Rule
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.params import State
from nonebot.typing import T_State
add_ = on_regex("^添加超管",rule=to_me())
del_ = on_regex("^删除超管",rule=to_me())
@add_.handle()
async def add_handler(bot:Bot,event:Event):
    id = event.get_user_id()
    txt = event.get_plaintext().strip()
    if "863109569" in id:
        bot.config.superusers.add(txt)
        await add_.finish("添加超管成功~")
    else:
        await add_.finish("你不是主人哦，无权添加")
@del_.handle()
async def del_handler(bot:Bot,event:Event):
    id = event.get_user_id()
    txt = event.get_plaintext().strip()
    if "863109569" in id:
        if txt in bot.config.superusers:
            bot.config.superusers.remove(txt)
            await del_.finish("删除超管成功~")
    else:
        await del_.finish("你不是主人哦，无权删除")