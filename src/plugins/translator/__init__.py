import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
import asyncio
from nonebot import on_message,on_request,on_regex
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent,FriendRequestEvent,GroupMessageEvent,GroupRequestEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import export
from nonebot.rule import Rule
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
def translate(s:str):
    try:
        cred = credential.Credential("AKIDAAuNaWCcmfGahW4KJ2UfYBXcRzGGzQbV", "e17wTjiRt4ybx2qNdbIiriIbeQvA9rIR")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-shanghai", clientProfile)

        req = models.TextTranslateRequest()
        Target = 'en'
        if  'a'<=s[0]<='z' or 'A'<=s[0]<='Z':
            Target = 'zh'
        params = {
            "SourceText": f"{s}",
            "Source": "auto",
            "Target": f"{Target}",
            "ProjectId": 0
        }
        req.from_json_string(json.dumps(params))

        resp = client.TextTranslate(req)
        return str(resp.TargetText)

    except TencentCloudSDKException as err:
        return '翻译出错了哦~'

translater = on_regex('^翻译',)

@translater.handle()
async def translater_handler(bot:Bot,event:Event):
    text = str(event.get_message())[2:].strip()
    if len(text)==0:
        await translater.finish(message="请输入要翻译的内容哦~")
    await translater.finish(message=f'{translate(text)}')