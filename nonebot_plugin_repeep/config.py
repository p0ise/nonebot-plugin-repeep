from pydantic import BaseSettings


class Config(BaseSettings):
    # api config
    trace_secret: str
    trace_api: str
    geoip_api: str
    ipuu_key: str

    # card style
    brief: str = "I Got U"
    url: str = "https://www.p0ise.cn/"
    title: str = "谁在窥屏"
    content: str = "抓住你了！"
    source: str = "I Got U"
    image: str = "random"

    class Config:
        extra = "ignore"
