# 技术来源与边界

Research-to-Decision 是 OpenInquire 的研究与决策升级。项目维护自己的中文入口、来源路由、平台读取与决策交付约定；研究执行复用 BMad 原版，不把上游的方法或代码称为自研。

## 随包提供的 BMad

- 上游：[bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
- 固定提交：[61e01f82644c4bb533750cfa0d6d61ab61d2cc9b](https://github.com/bmad-code-org/BMAD-METHOD/tree/61e01f82644c4bb533750cfa0d6d61ab61d2cc9b)
- 版本状态：上游 V7 Preview Alpha，模块记录 `6.13.0-next`。固定版本便于复查，不代表稳定版承诺。
- 目录：`bmad`、`bmod-core-tools`、`bmod-method`、`bmad-deep-recon`、`bmad-advanced-elicitation`、`bmad-review`。
- 上游原文件保持不变；每个目录附有原版 LICENSE、CONTRIBUTORS.md 和 TRADEMARK.md。文件及 SHA-256 清单见 [bmad-files.json](bmad-files.json)。BMad 名称归上游，本项目不代表上游背书或官方发行。
- 项目调整位于 `research-decide/`，通过 `assets/bmad-deep-recon.user.toml` 合并；不修改上游流程实现。

原版提供研究类型、Run / Process / Draft、Refresh / Deepen、引用与时间检查、需求澄清方法库和审阅流程。本项目增加面向日常选择的中文默认交付、按来源分工、查询转向说明、真实利弊区分和演示证据口径；固定候选数和无依据的打分不作为强制要求。

## 其余组件

| 组件 | 关系 |
| --- | --- |
| OpenInquire 平台研究、21 个只读 MCP 工具、本地助手 | 本仓库原有实现，保留其许可与来源说明 |
| `find-skills` | 可选候选发现工具，未捆绑；不改写其入口 |
| Octopus | 需求定义与 decision-support 的设计参考，未打包或运行其多模型系统 |
| Agent Reach、OpenCLI、DyNote、Groundwork | 平台接入、素材处理和研究组织的设计参考，不代表整套代码被合并 |
| last30days | 可另行安装的候选引擎；原有封装范围见安装与比较文档 |
| FFmpeg、faster-whisper 与平台适配器 | 外部运行依赖，按任务另装；不包含模型、登录状态或账号密钥 |

本项目没有训练专用模型，也不宣称用向量数据库或 RAG 实现了尚不存在的能力。多个 Agent 的观点一致不等于事实得到独立验证；底层来源和实际测试才是证据。验收范围见 [verification.md](verification.md)。
