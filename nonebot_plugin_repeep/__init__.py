from time import time
from asyncio import sleep
import httpx
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.adapters.onebot.v11 import escape
from nonebot import on_command
from nonebot import get_driver
from nonebot.log import logger

from .config import Config
from .ua_parse import get_device

global_config = get_driver().config
config = Config.parse_obj(global_config)

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

leakip = on_command("leakip", aliases={"谁在窥屏"})


@leakip.handle()
async def get_client():
    result = await get_key()
    if result['status'] == 1:
        logger.error("Incorrect Secrect")
        await leakip.send("密钥错误")
        return

    key = result['key']
    logger.success("Get Key: "+key)

    msg = share_csrf(key)
    try:
        await leakip.send(msg)
    except:
        logger.info("Failed to send XML info")
        await leakip.send("受tx风控，发送失败")
        return

    # sleep(1)
    await leakip.send("正在查询窥屏成分...")
    await sleep(3)
    # await leakip.send("等待完成...")

    result = await fetch_trace(key)
    if result['status'] == 1:
        logger.error("Incorrect Secrect")
        await leakip.send("密钥错误")
        return

    data = result['data']
    logger.success("Get Data: "+str(data))
    if not data:
        await leakip.send("没有查到 :(")
    else:
        msg_list = []
        for client in data:
            ua = client[0]
            ip = client[1]
            location = await get_geo(ip)
            logger.debug(f"IP Location:"+location)
            device = get_device(ua)
            logger.debug(f"Device:"+device)
            tpl = f"{location}有一名{device}用户正在窥屏"
            msg_list.append(tpl)

        msg = "\n\n".join(msg_list)
        await leakip.send(msg)


def share_csrf(key):
    url = config.url
    title = config.title
    content = config.content

    k = key + ".jpg"
    image = config.trace_api + "?k=" + k

    return Message(MessageSegment.share(url=url, title=title, content=content, image=image))


def xml_csrf(key):
    # card info
    brief = config.brief
    url = config.url
    title = config.title
    summary = config.content
    source = config.source

    k = key + ".jpg"
    cover = config.trace_api + "?k=" + k
    xml = f"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID='146' templateID='1' action='web' brief='{brief}' sourceMsgId='0' url='{url}' flag='0' adverSign='0' multiMsgFlag='0'><item layout='2' advertiser_id='0' aid='0'><picture cover='{cover}' w='0' h='0' /><title>{title}</title><summary>{summary}</summary></item><source name='{source}' icon='' action='app' appid='-1' /></msg>"""

    data = escape(xml)

    return Message(MessageSegment.xml(data=data))


def group_invite_csrf(key):
    # timestamp
    msgseq = "".join(str(time()).split("."))
    cover = config.image

    source = config.source
    k = key + ".jpg"
    icon = config.trace_api + "?k=" + k

    xml = f"""<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="128" templateID="12345" action="native" brief="&#91;链接&#93;邀请你加入群聊" sourceMsgId="0" url=""><item layout="2"><picture cover="{cover}"/><title>邀请你加入群聊</title><summary /></item><data groupcode="714652743" groupname="p0ise技术体验群" msgseq="{msgseq}" msgtype="2"/><source name="{source}" icon="{icon}" action="" appid="-1" /></msg>"""
    return Message(MessageSegment.xml(xml))


def cardimage_csrf(key):
    file = config.image
    source = config.source

    k = key + ".jpg"
    icon = config.trace_api + "/index.php?k=" + k

    cardimage = f"""[CQ:cardimage,file={file},source={source},icon={icon}]"""
    return Message(cardimage)


async def get_key():
    api = config.trace_api
    v = config.trace_secret

    url = api + "/key.php"
    params = {'v': v}
    r = httpx.get(url, params=params)
    result = r.json()
    return result


async def fetch_trace(k):
    api = config.trace_api
    v = config.trace_secret

    url = api + "/data.php"
    params = {'v': v, 'k': k}
    r = httpx.get(url, params=params)
    result = r.json()
    return result


async def get_geo(ip):
    api = config.geoip_api
    if api == "ipuu":
        result = await get_ipuu(ip)
        if result['code'] != "Success":
            pass
        else:
            data = result['data']

    location = ""
    if data:
        if data.get('country', ''):
            location += data['country']
            if data.get('prov', ''):
                if data.get('prov', '') != data.get('city', ''):
                    location += data['prov']
                if data.get('city', ''):
                    location += data['city']
                    if data.get('district', ''):
                        location += data['district']

    if not location:
        location = "未知地区"

    return location


async def get_ipuu(ip):
    key = config.ipuu_key

    url = "https://api.ipplus360.com/ip/geo/v1/district/"
    params = {'key': key, 'ip': ip}
    r = httpx.get(url, params=params)
    logger.debug(r.url)
    logger.debug(r.text)
    result = r.json()
    return result
