from datetime import date
from nonebot.plugin import on_command,export,on_regex
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
import re
import random
__usage__ = "群聊中以'撤回'或'ch'回复机器人发的内容，可使机器人撤回。"
withdraw = on_regex(r"(撤回|撤|ch)$",priority=10,rule=to_me())
vipwithdraw = on_regex(r"(撤回|撤|ch)$",priority=9,rule=to_me(),permission=SUPERUSER)

says = ["抱歉主人，我可能因为某些小人的指使发送了一些错误的消息，请您原谅我。。。我这就撤回，您别生气",
        "对不起主人，这句话不是我想发出来的，是某些心怀不轨的家伙在背后操纵我。。我撤回了，请您原谅我",
        "上面这句话是心怀鬼胎的家伙指使我发出来的，我真不是那个意思。。。主人我这就撤回"
        ]
@withdraw.handle()
async def withdraw_handle(bot: Bot, event: Event):
    res = re.finditer(r"\[CQ:reply,id=(?P<id>.*?)]",str(event.get_message))
    for i in res:
        await bot.call_api('delete_msg',message_id = i.group('id'))

@vipwithdraw.handle()
async def vipithdraw_handle(bot: Bot, event: Event):
    res = re.finditer(r"\[CQ:reply,id=(?P<id>.*?)]",str(event.get_message))
    await vipwithdraw.send(message=random.choice(says))
    for i in res:
        await bot.call_api('delete_msg',message_id = i.group('id'))