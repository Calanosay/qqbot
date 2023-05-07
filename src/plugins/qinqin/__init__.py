from datetime import date
from nonebot.plugin import on_command,export,on_regex
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.rule import to_me
import asyncio
import time
import re

qinqin = on_regex(r"^(\[CQ:face,id=109]|\[CQ:face,id=305]|贴贴)$",priority=30,rule=to_me())
@qinqin.handle()#亲亲
async def qinqin_handle(bot: Bot, event: Event):
    # if event.get_user_id in SUPERUSERS:await qinqin.finish(message = Message(f'主人[CQ:at,qq={event.get_user_id()}][CQ:face,id=109]'))
    await qinqin.finish(message = Message(f'[CQ:at,qq={event.get_user_id()}][CQ:face,id=109]'))