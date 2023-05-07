import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBot_V11_Adapter

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(OneBot_V11_Adapter)

nonebot.load_builtin_plugins('echo')
nonebot.load_plugin("nonebot_plugin_word_bank2")
nonebot.load_plugin('nonebot_plugin_covid19_news')
nonebot.load_plugin("nonebot_plugin_setu_now")
nonebot.load_plugin("nonebot_plugin_remake")
nonebot.load_plugin("nonebot_plugin_caiyunai")
nonebot.load_plugin("nonebot_plugin_youthstudy")
#nonebot.load_plugin("nonebot_plugin_tarot")
#nonebot.load_plugin("nonebot_plugin_fortune")
#nonebot.load_plugin("nonebot_plugin_petpet")
nonebot.load_plugins("src/plugins")
nonebot.load_plugin("nonebot_plugin_atri")
nonebot.load_plugin("nonebot_plugin_memes")
nonebot.load_plugin("nonebot_plugin_wordle")
nonebot.load_plugin("nonebot_plugin_handle")
if __name__ == "__main__":
    nonebot.run()