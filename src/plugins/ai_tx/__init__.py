import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
import asyncio
from nonebot import on_message,on_request,on_regex
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent,FriendRequestEvent,GroupMessageEvent,GroupRequestEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import export
from nonebot.rule import Rule
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
import random
ai_tx = on_message(priority=100,rule=to_me())
async def get_reply(s):
    try:
        cred = credential.Credential("AKIDAAuNaWCcmfGahW4KJ2UfYBXcRzGGzQbV", "e17wTjiRt4ybx2qNdbIiriIbeQvA9rIR")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

        req = models.ChatBotRequest()
        params = {
            "Query": f'{s}'
        }
        req.from_json_string(json.dumps(params))

        resp = client.ChatBot(req)
        return str(resp.Reply)

    except TencentCloudSDKException as err:
        return '闲聊功能出错了哦~'

@ai_tx.handle()
async def ai_txhandler(bot:Bot,event:Event):
    text = str(event.get_message()).strip()
    if 'image' in text:
        await ai_tx.finish(message=Message("不要发图给我捏，ay我又看不懂捏~"))
    if '[CQ:' in text:
         await ai_tx.finish(message=Message(f'[CQ:face,id={random.randrange(1,334)}]'))
    if len(text)==0:
        await ai_tx.finish(message="你想跟我聊什么呢~")
    reply = await get_reply(text)
    await asyncio.sleep(len(reply) / 20)
    await ai_tx.finish(message=f'{reply}')