# PPT as Code

> Clone 下来，用 Claude Code 打开，AI 自动引导你从零做出一套高质量 PPT。

一个 CLAUDE.md 驱动的 AI-人协作 PPT 工作台。AI 负责写 Prompt、生成图片、写记录；你负责选图、定方向、拍板。

## 效果展示

> 用本项目方法制作的职业规划竞赛 PPT（15 页，3D 渲染风格，70+ 次迭代）

![showcase](assets/showcase.png)

## 快速开始

### 准备

- [Claude Code](https://claude.ai/code) 或 [Cursor](https://cursor.sh)
- Python 3.8+
- 一个图片生成 API（推荐 Gemini，支持中文 Prompt + 参考图）

### 三步上手

```bash
# 1. Clone
git clone https://github.com/wzg7014/ppt-as-code.git my-ppt
cd my-ppt

# 2. 打开 Claude Code
claude

# 3. AI 会自动引导你完成：
#    → 配置 API 密钥
#    → 导入你的演讲稿/文案
#    → 确定视觉风格
#    → 逐页生成 PPT
```

你不需要看任何文档，打开就能用。AI 知道该做什么。

## 它是什么 / 不是什么

- **是** CLAUDE.md 驱动的 AI-人协作工作台
- **不是**全自动 PPT 生成器（AI 自嗨出来的图质量不行）
- **不是**纯文档/方法论（没有执行力）

核心理念：**人做决策，AI 干活**。

## 工作流程

```
Phase 1：项目初始化（AI 自动引导，只做一次）
    配置 API → 导入内容 → 确定视觉风格 → 分页规划
                              │
                              ▼
Phase 2：首版制作（逐页循环，每页一个对话）
    AI 写 Prompt → 生成 3 张候选 → 你选图 → 下一页
                              │
                              ▼ 拿去展示，收集反馈
Phase 3：迭代优化（针对性修改）
    收集反馈 → 写修改计划 → 逐页修改
```

每页制作时：
1. AI 读内容、写 Prompt、生成 3 张候选图
2. 你打开看，选最好的那张（或让 AI 调整后重新生成）
3. 确认后 AI 自动写记录、更新进度、Git 提交
4. 说"继续"做下一页

## 项目结构

### Clone 下来的样子

```
ppt-as-code/
├── CLAUDE.md                 # ⭐ 核心：AI 引导手册
├── .claude/commands/
│   └── done.md               # /done skill：完成当前页
├── tools/
│   └── gen_ppt_image.py      # 图片生成工具（纯 Python）
├── guide/                    # 方法论文档（选读）
│   ├── 01-philosophy.md      # 核心理念
│   ├── 02-workflow.md        # 完整工作流
│   ├── 03-prompt-patterns.md # Prompt 编写模式库
│   ├── 04-project-management.md
│   └── 05-iteration-strategy.md
├── README.md
├── LICENSE
└── .gitignore
```

### 使用后 AI 自动创建

```
├── .env                      # API 配置（不入 Git）
├── content/                  # 你的演讲稿/文案
├── progress.md               # 制作进度
├── ppt-ref-images/           # 参考图（风格锚定用）
└── ppt-pages/
    ├── 01/
    │   ├── init/             # 首版
    │   ├── rev1/             # 第一次修改（如有）
    │   └── rev2/             # 第二次修改（如有）
    └── 制作记录/
        ├── 首版/             # 每页首版制作记录
        └── 修改/             # 修改记录
```

## 为什么不是 Skill

Skill 是"AI 自己按规则执行"。PPT 制作中 **选图和定方向必须是人的决策**——AI 不知道哪张图更打动评委、哪个风格更适合你的故事。

CLAUDE.md 是"AI 和人共同遵守的项目规范"，它引导 AI 做该做的事（写 Prompt、跑脚本、写记录），同时 **在每个关键节点等待人的判断**。

## 竞品对比

| 维度 | 全自动 PPT 生成 | 本项目 |
|------|----------------|--------|
| 迭代管理 | 无 | 候选制（每页 3 张）+ 多轮决策树 |
| 项目管理 | 无 | CLAUDE.md + progress.md + 制作记录 |
| Prompt 经验 | 无 | 6 条铁律 + 持续积累 |
| 人机分工 | AI 全包 | AI 干活，人做决策 |
| 版本控制 | 无 | Git 按页提交 |
| 风格一致性 | 不保证 | 参考图机制 |

## 技术栈

- **AI 图像生成**：Gemini（支持中文 Prompt + 参考图上传）
- **AI 协作**：Claude Code / Cursor（通过 CLAUDE.md 驱动）
- **工具**：纯 Python，零外部依赖
- **版本控制**：Git

图片生成 API 可替换为任何兼容 Gemini 格式的服务。

## 方法论文档

想深入了解原理的，看 `guide/` 目录：

| 文档 | 内容 |
|------|------|
| [01-philosophy](guide/01-philosophy.md) | 为什么用代码做 PPT，核心概念 |
| [02-workflow](guide/02-workflow.md) | 三阶段工作流详解 |
| [03-prompt-patterns](guide/03-prompt-patterns.md) | Prompt 编写六条铁律 + 模式库 |
| [04-project-management](guide/04-project-management.md) | 项目管理、Git 规范、AI 协作边界 |
| [05-iteration-strategy](guide/05-iteration-strategy.md) | 迭代决策树、成本意识 |

## 贡献

欢迎提 Issue 和 PR。特别欢迎：

- 其他 AI 图像模型的适配
- 新的 Prompt 模式和技巧
- 真实项目案例分享

## License

MIT
