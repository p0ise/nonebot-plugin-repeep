<div align="center">
  <a href="https://github.com/p0ise/nonebot-plugin-repeep">
    <img src="https://static-cdn.p0ise.cn/local/logo.png" alt="Logo" width="80" height="80">
  </a>
  <h1 align="center">nonebot-plugin-repeep</h1>
  <p align="center">
    ✨ 一款基于nonebot2的插件，用于获取QQ中当前窥屏用户信息 ✨
    <br />
    <br />
  	<a href="https://raw.githubusercontent.com/p0ise/nonebot-plugin-repeep/main/LICENSE">
    	<img src="https://img.shields.io/github/license/p0ise/nonebot-plugin-repeep.svg" alt="license">
  	</a>
  	<a href="https://pypi.python.org/pypi/nonebot-plugin-repeep">
    	<img src="https://img.shields.io/pypi/v/nonebot-plugin-repeep.svg" alt="pypi">
  	</a>
  	<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
  </p>
</div>




<!-- TABLE OF CONTENTS -->

<details>
  <summary>目录</summary>
  <ol>
    <li>
      <a href="#关于">关于</a>
    </li>
    <li>
      <a href="#开始使用">开始使用</a>
      <ul>
        <li><a href="#前置条件">前置条件</a></li>
        <li><a href="#安装">安装</a></li>
        <li><a href="#配置项">配置项</a></li>
      </ul>
    </li>
    <li><a href="#用法">用法</a></li>
    <li><a href="#开发计划">开发计划</a></li>
    <li><a href="#原理">原理</a></li>
    <li><a href="#贡献">贡献</a></li>
    <li><a href="#LICENSE">LICENSE</a></li>
    <li><a href="#联系">联系</a></li>
    <li><a href="#致谢">致谢</a></li>
  </ol>
</details>


# 关于

本项目能够在QQ中获取当前窥屏用户的信息（目前只支持移动端QQ检测）。

> 截止至2022/11/24 22:30左右，群内获取IP的方法已经被和谐，暂时回退到只支持私聊的版本。

<p float="left">
  <img src="https://static-cdn.p0ise.cn/local/preview1.png" alt="preview1" width="200" />
  <img src="https://static-cdn.p0ise.cn/local/preview2.png" alt="preview2" width="200" /> 
  <img src="https://static-cdn.p0ise.cn/local/preview3.png" alt="preview3" width="200" />
</p>


> 由于本项目性质，使用的人多了之后检测接口随时会失效，且用且珍惜。

# 开始使用

## 前置条件

- CSRF信息记录后端
- IP定位接口

### CSRF后端

本项目的CSRF后端需要实现三个接口：

1. 获取Key（用于标识一个会话用于收集CSRF信息）
2. 渲染图片记录客户端信息
3. 取出收集到的信息

目前仅支持PHP实现的后端，具体搭建见[repeep-backend-php](https://github.com/p0ise/repeep-backend-php)。

### IP定位接口

目前采用[IPUU](https://mall.ipplus360.com/pros/IPVFourGeoAPI)提供的区县级定位接口，允许每天2000次免费调用，请开发者自行申请后将密钥填入配置项。

## 安装

使用 nb-cli 安装

```sh
nb plugin install nonebot-plugin-repeep
```

使用 pip 安装

```sh
pip install nonebot-plugin-repeep
```

## 配置项

配置方式：直接在 NoneBot 全局配置文件中添加以下配置项即可。

### 必填配置

#### CSRF后端

| 名称         | 类型  | 默认值 | 说明           |
| ------------ | ----- | ------ | -------------- |
| trace_secret | `str` | 无     | 后端接口的密钥 |
| trace_api    | `str` | 无     | 后端接口的URL  |

#### IP定位接口

| 名称      | 类型  | 默认值   | 说明                           |
| --------- | ----- | -------- | ------------------------------ |
| geoip_api | `str` | `"ipuu"` | 接口选项，目前仅支持`ipuu`接口 |
| ipuu_key  | `str` | 无       | `ipuu`接口密钥                 |

### 可选配置

#### XML样式

| 名称    | 类型  | 默认值                                                       | 说明            |
| ------- | ----- | ------------------------------------------------------------ | --------------- |
| brief   | `str` | `"I Got U"`                                                  | XML卡片简介     |
| url     | `str` | `"https://www.p0ise.cn/"`                                    | XML卡片跳转链接 |
| title   | `str` | `"谁在窥屏"`                                                 | XML卡片标题     |
| content | `str` | ``"抓住你了！"``                                             | XML卡片内容     |
| source  | `str` | `"I Got U"`                                                  | XML来源信息     |
| image   | `str` | `"https://static-cdn.p0ise.cn/2022/11/20221120180503774.jpg"` | XML图片         |

# 用法

- 发送 Command ：`谁在窥屏` 或者 `leakip`

# 开发计划

- [x] 优化IP位置数据精准度
- [ ] export插件信息和接口，以供其他插件使用
- [ ] 优化信息样式，拟采用HTML渲染输出图片
- [ ] 增加指令选项，指定获取目标群、用户信息
- [ ] 优化基于UA的设备识别
- [ ] 增加对电脑的检测
- [ ] 智能选择CSRF方法

# 原理

机器人基于python的nonebot2框架，QQ协议基于go-cqhttp。

插件实现原理是QQ的跨站请求伪造。通过图片调起GET方法访问接口，从而获取客户端IP和UA信息。

根据IP，获取定位信息。基于ipuu的在线接口。

根据UA，获取设备信息。基于user_agents库，增加中文优化和型号名称优化。

CSRF原理参考：https://cloud.tencent.com/developer/article/1933686

# 贡献

贡献使开源社区成为学习、启发和创造的绝佳场所。我们**非常感激**您所做的任何贡献。

如果您有建议可以使本项目更好，请 fork 存储库并创建一个拉取请求。您也可以简单地使用标签 "enhancement" 打开问题。别忘了给项目点一颗 Star！再次感谢！

1. Fork项目
2. 创建功能分支（`git checkout -b feature/AmazingFeature`）
3. 提交你的更改（`git commit -m 'Add some AmazingFeature'`'）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 打开拉取请求

# LICENSE

本项目采用 GPL 3.0 协议。更多信息请查看 `LICENSE`。

# 联系

博客：[p0ise's blog](https://www.p0ise.cn/)

项目地址：https://github.com/p0ise/nonebot-plugin-repeep

QQ交流群：https://jq.qq.com/?_wv=1027&k=eQPw3qT3

# 致谢

- [Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [nonebot / nonebot2](https://github.com/nonebot/nonebot2)
- [Y5neKO / qq_xml_ip](https://github.com/Y5neKO/qq_xml_ip)