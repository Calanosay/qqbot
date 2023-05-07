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

proname = on_regex("^取(外号|别名)")
getname = on_regex("^看本名")

@proname.handle()
async def proname_handler(bot: Bot, event: Event):
    temp = str(event.get_message()).split()
    if len(temp) != 3:
        await proname.finish("取外号请发送三段消息：取外号、本名、外号名~")

    name1 = temp[1].strip().casefold().title()
    name2 = temp[2].strip().casefold().title()
    names.setname(name2, name1)

    await proname.finish(f"{name1} 的外号已被设置为 {temp[2]} ~")

@getname.handle()
async def proname_handler(bot: Bot,event: Event):
    temp = str(event.get_message())[3:].strip().casefold().title()
    res = names.getname(temp)
    if res == -1:
        await getname.finish("这个外号还没有人使用哦~")
    await getname.finish(f"{temp} 的本名是 {res} 哦~")



