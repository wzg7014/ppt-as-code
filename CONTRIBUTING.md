# Contributing

欢迎给 PPT as Code 提 Issue 或 PR。这个项目还在早期，最需要真实使用反馈。

## 可以贡献什么

- 新的图片生成模型适配
- 更稳定的 Prompt 写法
- 真实 PPT 项目案例
- Claude Code、Codex、Cursor 的使用反馈
- README、guide、示例和错误处理改进

## 提 Issue

请尽量说明：

- 你想做什么类型的 PPT
- 使用的是哪个 agent
- 图片生成 API / 模型是什么
- 遇到的问题或希望新增的能力
- 如果是生成质量问题，附上 Prompt 和结果截图

## 提 PR

建议先开 Issue 说明方向。小改动可以直接提 PR。

PR 尽量满足：

- 只解决一个问题
- 文档和示例同步更新
- 不提交 `.env`、生成图片、个人项目内容
- 如果改了 `tools/`，请说明手动验证方式

## 本地检查

这个仓库目前没有完整测试套件。提交前至少检查：

```bash
python3 -m py_compile tools/gen_ppt_image.py
```

如果修改了 Markdown，请确认链接、路径和示例命令仍然可用。

## 维护原则

- 人做判断，AI 做执行
- 保留 Prompt 和迭代记录
- 不追求全自动，优先让流程可控
- 真实使用反馈比抽象功能更重要
