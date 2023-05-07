from datetime import date
from nonebot.plugin import on_command,export,on_regex
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.rule import to_me
import asyncio
import time
import re


advise = on_regex(r'^(建议|反馈)',priority=30,rule=to_me())
__usage__ = '给机器人发送“建议xxxx”或“反馈xxxx”，可给开发者提供建议'
__help__plugin_name__ = "提供建议" 

@advise.handle()
async def advise_handle(bot: Bot,event: Event):
    s = str(event.get_message())[len('建议'):].strip()
    await bot.call_api("send_group_msg",group_id = 904518362,message = f"[CQ:at,qq=863109569]主人，有一条来自于 QQ {event.get_user_id()} 的新建议:\n{s}")
    await advise.finish(message="成功给开发者提供建议，感谢您的支持!")