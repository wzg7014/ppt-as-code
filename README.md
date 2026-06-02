# PPT as Code

> 用 AI coding agent 做 PPT：把内容、视觉方向、Prompt、生成脚本和迭代记录都放进一个可维护的项目。

PPT as Code 是一个 AI-人协作的演示文稿工作台。它不是一键生成 PPT 的工具，而是把 PPT 制作拆成可追踪、可复用、可迭代的工程流程：

- 人负责内容判断、视觉方向和最终选择
- AI agent 负责拆页、写 Prompt、跑生成脚本、记录迭代
- Git 负责保存每一页的制作过程和版本变化

当前模板主要适配 Claude Code，也提供 `AGENTS.md`，方便 Codex、Cursor 等 coding agent 按同一套流程工作。

## 效果展示

用本项目方法制作的职业规划竞赛 PPT：15 页，3D 渲染风格，70+ 次迭代。

![showcase](assets/showcase.png)

## 适合谁

- 想用 AI 做高质量视觉型 PPT 的学生、创作者、开发者
- 需要反复打磨比赛、路演、汇报或提案的人
- 希望把 Prompt、图片生成和版本管理沉淀下来的团队

不太适合只做简单文字页、临时内部分享，或需要复杂动画的场景。

## 快速开始

### 准备

- Claude Code、Codex、Cursor 或其他能读取项目指令的 coding agent
- Python 3.8+
- 一个图片生成 API，推荐支持中文 Prompt 和参考图输入的模型

### 1. Clone

```bash
git clone https://github.com/wzg7014/ppt-as-code.git my-ppt
cd my-ppt
```

### 2. 打开 coding agent

Claude Code：

```bash
claude
```

Codex / Cursor：

```text
打开当前仓库，让 agent 读取 AGENTS.md 或 CLAUDE.md，然后说：
按项目指令初始化一个新的 PPT 项目。
```

### 3. 跟着引导走

AI 会引导你完成：

1. 配置图片生成 API
2. 导入演讲稿或文案
3. 确定视觉风格
4. 拆分页数
5. 逐页生成 3 张候选图
6. 由你选择、反馈、确认
7. 写入制作记录并提交 Git

## 工作流程

```text
Phase 1: 项目初始化
配置 API -> 导入内容 -> 确定视觉风格 -> 分页规划

Phase 2: 首版制作
读当前页内容 -> 写 Prompt -> 生成 3 张候选图 -> 用户选择 -> 记录并提交

Phase 3: 迭代优化
收集反馈 -> 写修改计划 -> 按页修改 -> 记录每轮迭代
```

核心原则：先做完整首版，再基于反馈逐页优化。

## 它解决什么问题

| 问题 | 传统做法 | 本项目做法 |
|------|----------|------------|
| 设计意图丢失 | 靠记忆和手动拖拽 | Prompt 记录视觉意图 |
| 版本混乱 | `最终版_v3_再改.pptx` | Git 按页提交 |
| 风格不一致 | 靠肉眼对齐 | 参考图和统一视觉规范 |
| AI 输出不可控 | 一次性生成整套 | 每页 3 张候选，人来拍板 |
| 经验难复用 | 做完就散 | guide 和制作记录沉淀方法 |

## 项目结构

```text
ppt-as-code/
├── AGENTS.md                  # Codex / Cursor 等 agent 的项目指令
├── CLAUDE.md                  # Claude Code 的项目指令
├── .claude/commands/
│   └── done.md                # 完成当前页时的记录和提交流程
├── tools/
│   └── gen_ppt_image.py       # 图片生成工具
├── guide/                     # 方法论文档
├── examples/                  # 输入内容示例
├── assets/
│   └── showcase.png
├── README.md
└── LICENSE
```

使用后会生成这些本地文件，默认不提交：

```text
.env                           # API 密钥
content/                       # 你的演讲稿或文案
progress.md                    # 制作进度
ppt-ref-images/                # 参考图
ppt-pages/                     # 每页生成结果和记录
```

## 方法论文档

| 文档 | 内容 |
|------|------|
| [01-philosophy](guide/01-philosophy.md) | 为什么用代码做 PPT |
| [02-workflow](guide/02-workflow.md) | 三阶段工作流 |
| [03-prompt-patterns](guide/03-prompt-patterns.md) | Prompt 编写模式库 |
| [04-project-management](guide/04-project-management.md) | 项目管理和 Git 规范 |
| [05-iteration-strategy](guide/05-iteration-strategy.md) | 迭代策略和成本意识 |

## 当前状态

这是一个早期开源模板，已经通过真实 PPT 项目验证过基本流程。现在优先维护这些方向：

- 支持更多图片生成模型
- 增加可复用示例项目
- 改进 Codex / Cursor 的 agent 指令
- 补充从 Markdown / 文案到页面规划的实践案例
- 完善自动检查和生成脚本的错误处理

路线图见 [ROADMAP.md](ROADMAP.md)。

## 贡献

欢迎提交 Issue 和 PR，尤其是：

- 其他图片模型的适配
- 更好的 Prompt 模式
- 真实 PPT 制作案例
- Codex、Cursor、Claude Code 的使用反馈
- 文档、示例和错误处理改进

贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## License

MIT
