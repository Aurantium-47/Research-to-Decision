# 使用原版 BMad 研究流程

依赖与本 skill 一起安装：`bmad`、`bmod-core-tools`、`bmod-method`、`bmad-deep-recon`、`bmad-review`、`bmad-advanced-elicitation`。它们是固定版本的上游原件。`chinese-platform-research` 负责按需获取平台资料。具体安装见仓库 `docs/installation.md`。

1. 从当前目录向上找最近的 `_bmad` 项目根；没有时以当前工作目录为根。
2. 读取相邻 `bmad/references/setup.md`，按它用 `uv run --no-cache <bmad>/scripts/setup.py --project-root <project> --skill <bmad> --root <skills-dir> --status` 检查。首次 setup 使用原脚本，不手造运行时；现有项目不自动迁移或清理。
3. 初始化后把本 skill 的 `assets/bmad-deep-recon.user.toml` 复制到项目 `_bmad/custom/bmad-deep-recon.user.toml`。已有文件先读取，只合并任务需要的设置，不覆盖个人修改。
4. 用项目 `resolve_customization.py --skill <bmad-deep-recon> --project-root <project> --key workflow` 解析配置。再读取并执行原版 `bmad-deep-recon/SKILL.md` 和对应模式文档。普通“帮我调研”默认 Run，已有报告选 Process，继续旧问题用 Refresh/Deepen。未指定 initiative 的日常问题默认 loose。
5. 配置和本入口明确覆盖原版的固定候选数量、强制评分及重复询问模式；保留必要需求讨论、证据获取、来源核验和原版报告结构。已有授权内的本地准备按宿主规则继续。

`bmad-advanced-elicitation` 的原版方法目录可以按类别读取，作为提出遗漏问题或反证的工具。借用方法不等于执行其完整交互流程；用户显式调用完整技能时保留原版交互。

`find-skills` 是可选候选发现组件。没有它也能通过网络检索与仓库核验完成工作。宿主没有平台登录或专用工具时，使用其他适合的可访问来源并留下缺口，不把登录态作为整个流程的必要条件。

原版 setup 的修复/迁移可能删除旧目录。遵守当前用户和宿主的文件操作规则；禁止删除时只检查并说明需要处理的具体路径，不自动清理。
