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

test = on_command("test", aliases={"测试", "测试风控"})
leakip = on_command("leakip", aliases={"谁在窥屏"})


@test.handle()
async def test_card():
    key = "deadbeef"
    imgurl = None
    if config.image == "random":
        imgurl = await random_image()
    msg = cardimage_csrf(key, imgurl)
    try:
        await leakip.send(msg)
    except:
        logger.info("Failed to send xml info")
        await leakip.send("受tx风控，发送失败")
        return


@leakip.handle()
async def get_client():
    result = await get_key()
    if result['status'] == 1:
        logger.error("Incorrect Secrect")
        await leakip.send("密钥错误")
        return

    key = result['key']
    logger.success("Get Key: "+key)

    imgurl = None
    if config.image == "random":
        imgurl = await random_image()
    msg = cardimage_csrf(key, imgurl)
    try:
        await leakip.send(msg)
    except:
        logger.info("Failed to send CardImage info")
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


def cardimage_csrf(key, imgurl=None):
    if imgurl != None:
        file = imgurl
    else:
        file = config.image
    source = config.source

    k = key + ".jpg"
    # icon = config.trace_api + "/index.php?k=" + k

    cardimage = f"""[CQ:cardimage,file={file},source={source}]"""
    return Message(cardimage)


def json_csrf(key):
    data = """{"app":"com.tencent.structmsg"&#44;"config":{"ctime":1669305900&#44;"forward":true&#44;"token":"c78dccb3d0c85fd1a9be55185526eb6b"&#44;"type":"normal"}&#44;"desc":"音乐"&#44;"extra":{"app_type":1&#44;"appid":100495085&#44;"msg_seq":16445981872477352116&#44;"uin":21296590}&#44;"meta":{"music":{"action":""&#44;"android_pkg_name":""&#44;"app_type":1&#44;"appid":100495085&#44;"ctime":1669305900&#44;"desc":"痛仰乐队"&#44;"jumpUrl":"https://y.music.163.com/m/song/28949129"&#44;"musicUrl":"http://music.163.com/song/media/outer/url?id=28949129"&#44;"preview":"http://p2.music.126.net/kAqWKIT-hYwO-jTS5BCAmQ==/8888451999121623.jpg"&#44;"sourceMsgId":"0"&#44;"source_icon":"https://i.gtimg.cn/open/app_icon/00/49/50/85/100495085_100_m.png"&#44;"source_url":""&#44;"tag":"网易云音乐"&#44;"title":"两个人的假期"&#44;"uin":21296590}}&#44;"prompt":"&#91;分享&#93;两个人的假期"&#44;"ver":"0.0.0.1"&#44;"view":"music"}"""
    return Message(MessageSegment.json(data=data))


def music_csrf(key):
    type_ = "163"
    id_ = 28949129

    return Message(MessageSegment.music(type_=type_, id_=id_))


def cmusic_csrf(key):
    url = "163"
    audio = "https://i.y.qq.com/v8/playsong.html?songid=384366071&songtype=0"
    title = config.title

    return Message(MessageSegment.music_custom(url=url, audio=audio, title=title))


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


async def random_image():
    result = await get_dmoe()
    if result['code'] == "200":
        imgurl = result['imgurl']

    return imgurl


async def get_dmoe():
    url = "https://www.dmoe.cc/random.php"
    params = {"return": "json"}
    r = httpx.get(url, params=params)
    logger.debug(r.text)
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
