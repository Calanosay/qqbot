import asyncio

import nonebot
from nonebot import on_message,on_request,on_regex
from nonebot.adapters.onebot.v11 import PRIVATE_FRIEND,Bot, Event, MessageEvent,FriendRequestEvent,GroupMessageEvent,GroupRequestEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import export
from nonebot.rule import Rule
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.params import State
from nonebot.typing import T_State
helper = on_regex(r'^(help)|(帮助)|(功能)$',permission=PRIVATE_FRIEND,priority=10)
show = on_regex(r'^show',permission=PRIVATE_FRIEND,priority=10)
help = {
    '1' : "发送'涩图'，'涩涩'，'色图'等，可看p站涩图,私聊‘涩图r18’可看18+涩图~",
    '2' : "给机器人发送'看股票 股票名'，即可看股票实时估值；发送'关注'或'监控'或'jk'可令机器人为你持续关注某一股票。监控最后还可加上 通知波幅阈值，此值默认0.3，监控时后面不跟数字即为此值。若股票距离上次的涨跌幅超过该值，机器人会通知你。",
    '3' : "群聊内发送‘续写 ....’，可对内容进行续写",
    '4' : "发送remake，可开始人生重开（建议私聊，群聊容易风控，发不出",
    '5' : "发送’..疫情‘，'..疫情政策'，可分别查询某地疫情和疫情政策",
    '6' : "发送'..天气'，可查询某地七天内天气预报",
    '7' : "发送jrrp，可查询今日人品",
    '8' : "请查看空间说说内容，目前仅群管、私聊、开发者有权限使用.",
    '9' : "群内使用‘回复’功能，以‘撤回’或‘ch’回复机器人的某条消息，可使机器人自动撤回该消息",
    '10' : "发送'青年大学习'或'大学习'，可获取最新一期大学习答案",
    '11' : "可以发送‘头像表情包’以及‘表情包制作’来了解详细具体内容，头像表情包后面可跟qq，图片等，表情包制作只能跟文字。",
    '12' : "发送'翻译....'可自动进行英汉互译,如果是其他语言则默认翻译为英文。",
    '13' : "发送“猜单词”可开始猜单词,发送“结束”以结束游戏，发送“提示”以获取提示，可使用”-l“来指定单词长度，可使用”-d“来指定词典",
    '14' : "在群聊中发送“看卷王xxx”可监视此人洛谷做题，新做题会有群内播报；发送“看cf卷王xxx”可监视此人cf做题；发送”停看卷王xxx“以及“停看cf卷王xxx”可取消洛谷和cf对应卷王的监视；",
    '15' : """1.自动同意添加好友好友、群邀请请求
2.自动保存你们发的闪照
3.特定群聊自动+1
4.开发者群聊对bot发送'你给我滚出去'，自动滚蛋（引用开发者物理课上的遭遇
5.发送’建议 xxxx‘自动把建议转发给开发者
6.自带ai聊天系统,前面所有命令匹配失败会自动进入ai"""
}
@helper.handle()
async def helper_handler(bot:Bot,event:MessageEvent):
    await helper.send(message=Message("""隔壁老♂y🚹自动涩涩机器人~
别称:"ay","阿y","小y","yls","老y"                
在群聊时叫我开头需要加上别称哦~(私聊不用)
功能如下:
1.看涩图
2.看盘小助手
3.小梦续写(私聊无效)
4.玩人生重开
5.查询疫情
6.查询天气
"""))
    await helper.send(message=Message("""
7.今日人品
8.关键词词库
9.撤回消息
10.青年大学习
11.表情包制作
12.中英互译
13.猜单词
14.算法竞赛相关功能
15.被动技能和杂项
发送show + 选项编号即可查看详细用法~ (不用加'+')
"""))
@show.handle()
async def show_handler(bot:Bot,event:Event,state:T_State = State()):
    num = str(event.get_plaintext())[4:].strip()
    if num not in help:
        await show.finish(message=Message("请输入合法序号[CQ:face,id=262]"))
    await show.finish(message=Message(help[num]))