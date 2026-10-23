# 安装与配置

## 完整调研与决策包

下载或克隆本仓库后，将下列 **8 个目录一起**放进宿主支持的 skills 目录：

```text
research-decide
chinese-platform-research
bmad
bmod-core-tools
bmod-method
bmad-deep-recon
bmad-advanced-elicitation
bmad-review
```

Codex 默认位置是用户目录下 `.codex/skills`；自定义了 `CODEX_HOME` 则使用其 `skills` 子目录。同名目录已有内容时先比较，保留个人修改，不直接覆盖。`bmod-*` 是原版模块元数据，不是用户直接调用的技能；这里没有安装 BMad 全套软件开发工作流。

安装 [uv](https://docs.astral.sh/uv/getting-started/installation/) 后，在要研究的项目中说：

> 使用 `$research-decide`，初始化这里的 BMad 研究环境，帮我调研【问题】并选出适合我的方案。

入口会用原版 setup 初始化 `_bmad`，读取项目设置并合并随包提供的中文决策配置。实际报告写在当前项目，不写进技能安装目录。日常可直接说“调研抉择”或“利弊抉择 skill”；纯平台材料任务用 `$chinese-platform-research`。宿主未刷新技能列表时，重新加载会话。

**最低运行条件：**能读取本地技能并执行命令的 Agent、`uv`、进行 Run 时可用的网络检索工具。Windows 已做隔离目录运行检查；该流程不依赖 WSL。它使用宿主模型与工具，不自带模型或搜索服务。多 Agent 研究需要宿主支持并允许并行；没有对应能力时不能声称执行过独立评审。单次模型、搜索或付费数据成本取决于所用服务。

`find-skills` 可选；没有它可以直接查技能目录和 GitHub。浏览器、中文平台登录、专用适配器和视频模型按任务接入，不是每个决策都要装。详细原版接入步骤见 [BMad 接入说明](../skills/research-decide/references/bmad-integration.md)，版本及许可见[第三方来源](third-party.md)。

## 平台读取、MCP 与视频能力

按任务选择组件：先安装 Skill，再连接需要的浏览器、MCP 或视频处理环境。

| 组件 | 包含在本仓库 | 前提 |
| --- | --- | --- |
| 调研Skill、两段本地助手脚本 | 是 | 支持Skill的宿主；Python3.12已验收 |
| 技术社区只读MCP（21工具） | 是 | Python3.12与 `mcp/requirements.txt` |
| 日常浏览器读取中文平台 | 否 | 宿主支持的浏览器扩展、相应站点正常登录 |
| 微信指定分享会话 | 否 | 宿主另配桌面 Computer Use 插件、正常登录与本次指定的读取范围 |
| B站/公众号专用适配器 | 否 | 单独安装和验证，见渠道文档 |
| last30days候选引擎 | 否，可选 | 独立安装的上游代码；封装只启用HN/GitHub |
| 视频本地处理 | 助手脚本是 | FFmpeg/FFprobe、Pillow；转写另需faster-whisper和完整本地模型 |

将 `skills/chinese-platform-research` 目录安装到宿主用户级skills目录。例如Codex常用 `$CODEX_HOME/skills`，未自定义时为用户目录下 `.codex/skills`。同名已存在时先比较并合并，避免覆盖个人更新。

在仓库根目录为可选MCP创建独立环境：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r mcp/requirements.txt
.\.venv\Scripts\python.exe mcp/server.py
```

macOS/Linux用 `python3.12`、`.venv/bin/python` 对应替换；本轮未实测这些系统。服务使用stdio，不监听公开端口。将宿主MCP配置中的command设为该虚拟环境Python绝对路径，args设为 `server.py` 绝对路径。不要照抄别人的个人目录，也不覆盖现有MCP配置。

```json
{
  "command": "<绝对路径>/.venv/Scripts/python.exe",
  "args": ["<绝对路径>/mcp/server.py"]
}
```

这是通用stdio字段示例；外层配置格式以当前宿主为准。连接后先列工具，再运行小样本，`platform_access_status`只检查配置，不是联网验收。

视频依赖按需要安装在所用Python环境：

```powershell
py -3.12 -m pip install Pillow faster-whisper
py -3.12 skills/chinese-platform-research/scripts/read_video_local.py '<媒体路径>' --out '<全新输出目录>' --model '<完整本地模型目录>' --source-url '<原作网址>'
```

FFmpeg/FFprobe需在PATH中。模型须为faster-whisper可用目录；脚本不自动下载模型。已有字幕或无音轨视频用 `--no-asr`，仅处理音频可用 `--no-frames`。
