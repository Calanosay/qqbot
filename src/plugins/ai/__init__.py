# import requests
# import re
# import random
# 
# from nonebot import on_command, on_message, on_regex, export
# from nonebot.permission import SUPERUSER
# from nonebot.typing import T_State
# from nonebot.adapters.onebot.v11.bot import Bot
# from nonebot.adapters.onebot.v11.message import Message
# from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent,Event
# from nonebot.adapters.onebot.v11.utils import unescape
# from nonebot.params import State
# from nonebot.rule import to_me
# ai = on_message(priority=100,rule=to_me())
# 
# 
# def get_mes(ques,qq):
#     api = "9064bec2-ba92-4785-9b3b-e3a10c50104c"
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
#     }
#     url = f"http://api.ruyi.ai/ruyi-api/v1/message?app_key={api}&user_id={qq}&q={ques}"
#     text = requests.get(url=url,headers=headers).text
#     res = re.finditer("\"text\":\"(?P<ans>.*?)\"",text)
#     idx = 0
#     for i in res:
#         idx += 1
#         if idx == 1:
#             continue
#         return (i.group("ans"))
# def handle_mes(ques):
#     ques = ques.strip()
#     ques = ques.replace('\\\\n','')
#     ques = ques.replace('\\n','')
#     ques = ques.replace('\\r','')
#     ques = ques.replace('\\','')
#     return ques
# 
# @ai.handle()
# async def ai_handler(bot:Bot,event:Event,state:T_State=State()):
#     ques=str(event.get_message()).strip()
#     man = event.get_user_id()
#     if 'image' in ques:
#         await ai.finish(message=Message("哎，不要发图给我捏，ay我又看不懂捏~"))
#     if '[CQ:' in ques:
#         await ai.finish(message=Message(f'[CQ:face,id={random.randrange(1,334)}]'))
#     ques=get_mes(ques,man)
#     ques=handle_mes(ques)
#     await ai.finish(message=Message(ques))
# 
