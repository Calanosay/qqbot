import asyncio

from nonebot import on_message,on_request,on_regex
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent,FriendRequestEvent,GroupMessageEvent,GroupRequestEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import export
from nonebot.rule import Rule
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER

self_add = on_request(priority=60)

gun_group = on_regex('(滚出去!|滚出去)$',priority=1,rule=to_me(),permission=SUPERUSER)

reply = on_regex('^回复',rule=to_me(),permission=SUPERUSER,block=False,priority=2)
__usage__ = '被动技能，加入人数超过500人群后会自动退出'
__help__plugin_name__ = "自动加群、好友"
@reply.handle()
async def reply_handler(bot:Bot,event:Event):
    text = str(event.get_message()).strip()
    text = text[len('回复'):]
    start = 0
    for i in text:
        if i.isdigit():start+=1
        else:break
    qq=text[0:start]
    text = text[start:]
    if(len(qq) < 5 or len(qq) > 13):reply.block=False
    else:
        reply.block=True
        try:
            await bot.call_api('send_private_msg', user_id=qq, message=Message(f"您收到一条来自主人的消息:\n{text}\n\n如需回复,请以提建议的形式发送:\"建议...\""))

        except:
            await reply.send(message="消息发送失败。")
        else:await reply.send(message="消息发送成功~")

@gun_group.handle()
async def gun_handler(bot:Bot,event: GroupMessageEvent):
    gp_id = event.group_id
    await gun_group.send(message=Message("这...这就滚..."))
    await asyncio.sleep(3)
    await bot.call_api('set_group_leave', group_id=gp_id)

@self_add.handle()
async def ad_f(bot: Bot, event: FriendRequestEvent):
    await event.approve(bot)
    id = int(event.get_user_id())
    await asyncio.sleep(1)
    await bot.call_api('send_private_msg',user_id=id,message=Message('哈喽，我是ay，请发送help获取我的菜单，菜单最后三行内容请不要忘了看。有新的消息，注意事项会发空间告知。如果想联系主人的话，请私聊发送‘建议xxxx’来提交你的反馈。'))

@self_add.handle()
async def ad_f(bot: Bot, event: GroupRequestEvent):
    if event.sub_type == 'invite':
        await event.approve(bot)
        gp_id = int(event.group_id)
        await asyncio.sleep(5)
        inviter = int(event.get_user_id())
        num = (await bot.call_api('get_group_info', group_id=gp_id))['member_count']
        if num > 500:
            await bot.call_api('set_group_leave', group_id=gp_id)
            await bot.call_api('send_private_msg', user_id=inviter, message=Message("抱歉,群人数超过500,我不能同意进入该群"))
