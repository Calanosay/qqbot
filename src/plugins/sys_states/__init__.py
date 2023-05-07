from nonebot.adapters.onebot.v11 import Bot, Event, PokeNotifyEvent
from nonebot.plugin import export, on_notice
from nonebot.rule import Rule
from nonebot.permission import Permission,SUPERUSER
from .info_get import get_sys_info


export = export()
export.name = '系统状态'
export.usage = '戳一戳以获取系统当前状态'



async def _is_poke(bot: Bot, event: Event) -> bool:
    return isinstance(event, PokeNotifyEvent) and event.is_tome()

sys_info = on_notice(Rule(_is_poke), priority=50, block=True)
@sys_info.handle()
async def sys_info_handle(bot: Bot, event: Event):
    info = get_sys_info('b')
    await sys_info.send(info)
#hint_msg = '如果想要获取更多信息，请输入对应的模式名。\n全部信息：a\n简要信息：b\n输入其他信息则不再继续查询。'
#@sys_info.got('method',prompt=hint_msg)
#async def sys_info_got(bot: Bot, event: Event, state: T_State):
#    method = state["method"]
#    info = get_sys_info(method)
#    await sys_info.finish(info)



