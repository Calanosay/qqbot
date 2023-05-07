import asyncio

from nonebot import on_message, on_request, on_regex, on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, MessageEvent, FriendRequestEvent, GroupMessageEvent, \
    GroupRequestEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import export
from nonebot.rule import Rule
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.params import T_State, State
import re
import time


def to_int64(x: str):
    res = 0
    l = len(x)
    for i in range(0, l, 1):
        res = res * 10 + int(x[i])
    return res


yuyin = on_regex('^说', rule=to_me())
good_night = on_regex('^晚安', rule=to_me(), priority=4, block=True)


@good_night.handle()
async def send_good_night(bot: Bot, event: Event):
    hour = time.localtime().tm_hour
    if hour >= 22 or hour <= 6:
        fil = re.compile(u'[^0-9a-zA-Z\u4e00-\u9fa5.，,。？“”]+', re.UNICODE)
        name = fil.sub(' ', event.sender.card) or fil.sub(' ', event.sender.nickname)
        text = fil.sub(' ', name) + "，晚安。"
        message = Message(f'[CQ:tts,text={text}]')
        await good_night.finish(message)
    else:
        text = str(f'才{str(hour - 12)}点，晚安你妈呢')
        await good_night.finish(message=Message(f'[CQ:tts,text={text}]'))


@yuyin.handle()
async def wangjing_handler(bot: Bot, event: Event):
    text = str(event.get_message()).strip()[1:]
    await yuyin.finish(message=Message(f'[CQ:tts,text={text}]'))


qunyuyin = on_regex('^群语音', permission=SUPERUSER)
siliaoyuyin = on_regex('^私聊语音', permission=SUPERUSER)


@qunyuyin.handle()
async def qunyuyin_handler(bot: Bot, event: Event):
    text = str(event.get_message()).strip()
    text = text[3:]
    text = text.strip()
    start = 0
    for i in text:
        if i.isdigit():
            start += 1
        else:
            break
    qq = text[0:start]
    text = text[start:]
    await qunyuyin.send(message=f'成功执行群号{qq}')
    await bot.send_group_msg(group_id=to_int64(qq), message=Message(f'[CQ:tts,text={text}]'))


@siliaoyuyin.handle()
async def siliaoyuyin_handler(bot: Bot, event: Event):
    text = str(event.get_message()).strip()
    text = text[4:]
    text = text.strip()
    start = 0
    for i in text:
        if i.isdigit():
            start += 1
        else:
            break
    qq = text[0:start]
    text = text[start:]
    await siliaoyuyin.send(message='成功执行')
    await bot.send_private_msg(user_id=to_int64(qq), message=Message(f'[CQ:tts,text={text}]'))