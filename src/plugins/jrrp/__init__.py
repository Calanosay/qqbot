import random
from datetime import date
from nonebot.plugin import on_command, export, on_regex
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.rule import to_me

export = export()
export.name = '今日人品'
export.usage = '''https://www.bilibili.com/read/cv11108712'''
__usage__ = '给机器人发送jrrp，可抽取今日人品'
__help__plugin_name__ = "今日人品"


def luck_simple(num):
    if num < 20:
        return '大凶'
    elif num < 30:
        return '凶'
    elif num < 40:
        return '忧虞'
    elif num < 50:
        return '小疵'
    elif num < 60:
        return '中平'
    elif num < 65:
        return '末吉'
    elif num < 70:
        return '小吉'
    elif num < 80:
        return '吉'
    elif num < 90:
        return '大吉'
    else:
        return '元吉'


jrrp = on_regex(r'^(jrrp|今日人品)$', priority=50, rule=to_me())


@jrrp.handle()
async def jrrp_handle(bot: Bot, event: Event):
    rnd = random.Random()
    rnd.seed((int(date.today().strftime("%y%m%d")) * 45) * (int(event.get_user_id()) * 55))
    lucknum = rnd.randint(1, 100)
    if event.get_user_id() == "863109569":
        await jrrp.finish(message=Message(f'[CQ:at,qq={event.get_user_id()}]您今日的幸运指数是999/100，为"吉尼实在是太美"'))
    await jrrp.finish(
        message=Message(f'[CQ:at,qq={event.get_user_id()}]您今日的幸运指数是{lucknum}/100，为"{luck_simple(lucknum)}"'))