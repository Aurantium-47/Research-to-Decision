# 公众号文章读取与归档

本页整合单独安装的 `mcp-server-wechat` 与 WxArticleSaver 的读取和归档流程。只在任务涉及微信公众号时读取。两个适配器均需另行安装；正文读取接口见[上游MCP](https://github.com/odyecho/mcp-server-wechat)，图文导出见[WxArticleSaver](https://github.com/shanliuling/WxArticleSaver)。

以下是正常可访问情况下的工具路线，不能用于绕过当前工具明确的站点安全拒绝；历史样本成功不表示当前读取已获准或一定可用。

## 路由

1. 没有文章直链：用 `wechat_public` 的 `search_public_articles` 发现候选。不要用搜索摘要代替原文。
2. 已有 `https://mp.weixin.qq.com/s/<id>`：优先调用 `mcp-server-wechat` 的 `get_public_article_content` 读取正文。
3. 用户要求本地保存、图片资源或微信 WebView 内文章：使用 WxArticleSaver。普通文章可先尝试无代理的解析导出；需要 WebView 网络流量、视频资源或直接在微信中操作时使用完整代理流程。

直接保留用户给的原链接。`mcp-server-wechat` 的链接支持取决于安装版本及本地修补；开发环境曾静态核到同时接受 `/s/<id>` 与 `/s?...`，这不等于所有长链接都可读。保留长链接的完整查询/签名参数。另一安装版本若仍报格式拒绝，先核其校验实现；需要短链时再通过文章正常“复制链接”取得，不擅自删改参数或猜相似字形。

## 读取失败时先定位发生在哪一层

| 实际证据 | 能下的判断 | 接续方式 |
| --- | --- | --- |
| 浏览器 `ERR_CONNECTION_CLOSED`、超时，或HTTP客户端传输异常 | 本次连接失败；尚不能确定是网络、服务器还是客户端，也不证明文章失效 | 在没有明确策略拒绝的前提下，做有界普通重试或用已配置的正常读取渠道；不据一次失败重装整个方案 |
| 页面显示登录、验证码或访问频率提示 | 正文尚未取得；这是站点交互/访问条件 | 由用户完成需要本人操作的步骤，之后只在工具允许的正常正文页继续；不保证人工验证会解除工具层限制 |
| 工具明确返回站点安全策略拒绝 | 当前工具不允许该读取；不是解析器报错，除非工具明确说明，也不是Auto-review拒绝 | 停止对同一目标改工具、接口、浏览器或镜像重试。用户已完成验证后若仍被拒绝，不重复要求验证；可分析用户直接提供的文字/文件，并标清来源 |
| 获准取得正常文章HTML，但标题/正文选择器为空，或工具仅报通用解析错误 | 可能是页面结构/提取器问题；不能自行判定删除、验证码或失效 | 查看已获准的HTML/DOM与解析器所匹配的选择器；需要修解析器时才改代码，再用正常文章及错误页样本验收 |

状态同时记录目标URL、使用渠道、是否拿到正文及错误原文。只把原页面明确返回的删除/失效提示记为文章失效。工具的通用报错里列出的几种“可能原因”不是实际诊断。

连接器可能返回缓存；再次调用同一URL不自动成为新的网络连通性验证。用户提供的正文与工具取得的原文分别保存，后者失败不会使前者不能用于研究；不能把用户贴文记成已解除浏览器限制。

## MCP 正文读取

调用参数：

```json
{
  "input": {
    "article_url": "https://mp.weixin.qq.com/s/ARTICLE_ID",
    "format": "json",
    "detail": "detailed",
    "extract_images": true
  }
}
```

成功必须同时满足：返回 URL 与目标一致；标题不是空值或“无标题”；正文是有意义的文章内容而不是验证码、安全检查、登录页或“无法获取文章内容”；字数合理。需要图片时还要检查图片 URL。

不要在用户已有直链时先走搜狗。实测搜索可能返回相对 `/link?...`，继续跳转会触发 anti-spider 页面。访问频率受限时停止快速重试。

MCP 的作者选择器可能返回“未知作者”，而 WxArticleSaver 能识别同页作者；作者身份影响结论时交叉核对。Windows 终端显示中文乱码时，先用 `json.dumps(..., ensure_ascii=True)` 或读取 UTF-8 输出文件判断是显示问题还是数据损坏。

## WxArticleSaver 完整流程及授权

以下操作是否已有授权，以当前用户、当前任务和工具要求为准；不能把原作者或另一会话的授权当作安装本Skill即获得的永久权限。任务确实需要完整代理流程时，先检查是否已有针对这些操作的有效授权；已有授权不重复询问：

- 克隆或更新 `odyecho/mcp-server-wechat`、`shanliuling/WxArticleSaver`，并在隔离环境安装仓库声明的依赖；
- 安装 WxArticleSaver 在本机生成的 CA；
- 按该项目方式临时修改 Windows 系统代理；
- 完全退出并重新打开微信。

只操作明确授权范围，不扩大到第三方证书、远程代理、关闭安全防护或其他软件流量。使用上游项目或已检查的本地 checkout，代理只监听 localhost；修改前保留原代理状态，正常退出或失败后恢复。不能绕过 Windows 的交互确认；遇到 UAC、证书确认或凭据提示时请用户亲自完成。结束后报告代理是否恢复、CA 是否仍保留，以及项目提供的移除方式。

正常 UI 路径：启动 WxArticleSaver，按需要重启微信，打开公众号文章；按钮未出现时刷新；点击“导出本文”。验证导出目录存在 `article.md`、`article.html`、`article.txt`、`meta.json`，并报告图片数量及 `videos_found`、`videos_downloaded`。不能把“发现视频”写成“已下载视频”。

## 无代理复用导出核心

仅在已有公开直链、且不需要 WebView 捕获或视频发现时使用。设置 `WXAS_EXPORT_DIR` 必须早于导入模块，因为 `EXPORT_ROOT` 在导入时确定。默认 Requests User-Agent 可能得到缺少 `#js_content` 的另一种 HTTP 200 页面，使用浏览器式 User-Agent，并验证正文选择器。

```python
import json
import logging
import os

os.environ["WXAS_EXPORT_DIR"] = r"C:\path\to\exports"

import requests
import wx_article_saver as wx

url = "https://mp.weixin.qq.com/s/ARTICLE_ID"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
}

# save_article 通常在 mitmproxy 中运行，脱离该上下文时补日志对象。
wx.ctx.log = logging.getLogger("wxas")
response = requests.get(url, headers=headers, timeout=60)
response.raise_for_status()
response.encoding = "utf-8"
folder, title, downloaded_videos = wx.save_article(url, response.text, [])
meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
print(json.dumps(meta, ensure_ascii=True))
```

空的 `captured_media` 不能恢复只在实时 WebView 网络流量中出现的视频 URL。HTTP 200 也不代表成功，验证码和验证页同样可能返回 200。导出前应确认 `find_article_content()` 命中 `#js_content` 或其他受支持正文选择器；导出后检查 `meta.json` 的 `text_chars`、`images_downloaded`、`videos_found`、`videos_downloaded`，并抽查 `article.md` 开头。

## 实测基线

2026-09-20，同一篇公开 `/s/<id>` 文章经真实 MCP `call_tool` 返回标题和 5,786 个正文字符；无代理复用 WxArticleSaver 导出核心命中 `#js_content`，生成 Markdown/HTML/TXT/元数据并下载 26/26 张图片。该样本无视频。搜狗发现路径触发反爬，而直接 URL 读取成功。

2026-10-12，一条短链在Edge连接关闭后由既有MCP返回10,836字符及84个图片URL；另一条在人工作完验证、回到正常标题页后仍被浏览器工具策略拒绝，改分析用户主动贴入的正文。这两项分别证明正常连接器仍有可用样本、人工验证不保证工具放行；没有重试被拒绝目标或修改代理/证书。若安装版本存在本地修补，更新前保留并比较，不假定上游HEAD与本机基线一致。
