# Antigravity Skills

通过模块化的 **Skills** 定义，赋予 Agent 在特定领域的专业能力（如全栈开发、复杂逻辑规划、多媒体处理等），让 Agent 能够像人类专家一样系统性地解决复杂问题。

## 📂 目录结构

```
.
├── .agent/
│   └── skills/             # Antigravity Skills 技能库
│       ├── skill-name/   # 独立技能目录
│       │   ├── SKILL.md    # 技能核心定义与Prompt（必须）
│       │   ├── scripts/    # 技能依赖的脚本（可选）
│       │   ├── examples/   # 技能使用示例（可选）
│       │   └── resources/  # 技能依赖的模板与资源（可选）
├── skill-guide/            # 用户手册与文档指南
│   └── Antigravity_Skills_Manual_CN.md  # 中文使用手册
└── README.md
```

## 📖 快速开始
1. 将`.agent/`目录复制到你的工作区：
```bash
cp -r .agent/ /path/to/your/workspace/
```
2. **调用 Skill**: 在对话框输入 `@[skill-name]` 或 `/skill-name`来进行调用，例如：
```text
/canvas-design 帮我设计一张关于“Deep Learning”的博客封面，风格要素雅、科技感，尺寸 16:9
```
3. **查看手册**: 详细的使用案例和参数说明请查阅 [skill-guide/Antigravity_Skills_Manual_CN.md](skill-guide/Antigravity_Skills_Manual_CN.md)。
4. **环境依赖**: 部分 Skill (如 PDF, XLSX) 依赖 Python 环境，请确保 `.venv` 处于激活状态或系统已安装相应库。


## 🚀 已集成的 Skills

### 🎨 创意与设计 (Creative & Design)
这些技能专注于视觉表现、UI/UX 设计和艺术创作。
- **`@[algorithmic-art]`**: 使用 p5.js 代码创作算法艺术、生成艺术
- **`@[canvas-design]`**: 基于设计哲学创建海报、艺术作品（输出 PNG/PDF）
- **`@[frontend-design]`**: 创建高质量、生产级的各种前端界面和 Web 组件
- **`@[ui-ux-pro-max]`**: 专业的 UI/UX 设计智能，提供配色、字体、布局等全套设计方案
- **`@[web-artifacts-builder]`**: 构建复杂、现代化的 Web 应用（基于 React, Tailwind, Shadcn/ui）
- **`@[theme-factory]`**: 为文档、幻灯片、HTML 等生成配套的主题风格
- **`@[brand-guidelines]`**: 应用 Anthropic 官方品牌设计规范（颜色、排版等）
- **`@[slack-gif-creator]`**: 制作专用于 Slack 的高质量 GIF 动图

### 🛠️ 开发与工程 (Development & Engineering)
这些技能涵盖了编码、测试、调试和代码审查的全生命周期。
- **`@[test-driven-development]`**: 测试驱动开发（TDD），在编写实现代码前先编写测试
- **`@[systematic-debugging]`**: 系统化调试，用于解决 Bug、测试失败或异常行为
- **`@[webapp-testing]`**: 使用 Playwright 对本地 Web 应用进行交互测试和验证
- **`@[receiving-code-review]`**: 处理代码审查反馈，进行技术验证而非盲目修改
- **`@[requesting-code-review]`**: 主动发起代码审查，在合并或完成任务前验证代码质量
- **`@[finishing-a-development-branch]`**: 引导开发分支的收尾工作（合并、PR、清理等）
- **`@[subagent-driven-development]`**: 协调多个子 Agent 并行执行独立的开发任务

### 📄 文档与办公 (Documentation & Office)
这些技能用于处理各种格式的专业文档和办公需求。
- **`@[doc-coauthoring]`**: 引导用户进行结构化文档（提案、技术规范等）的协作编写
- **`@[docx]`**: 创建、编辑和分析 Word 文档
- **`@[xlsx]`**: 创建、编辑和分析 Excel 电子表格（支持公式、图表）
- **`@[pptx]`**: 创建和修改 PowerPoint 演示文稿
- **`@[pdf]`**: 处理 PDF 文档，包括提取文本、表格，合并/拆分及填写表单
- **`@[internal-comms]`**: 起草各类企业内部沟通文档（周报、通告、FAQ 等）
- **`@[notebooklm]`**: 查询 Google NotebookLM 笔记本，提供基于文档的确切答案

### 📅 计划与流程 (Planning & Workflow)
这些技能帮助优化工作流、任务规划和执行效率。
- **`@[brainstorming]`**: 在开始任何工作前进行头脑风暴，明确需求和设计
- **`@[writing-plans]`**: 为复杂的多步骤任务编写详细的执行计划（Spec）
- **`@[planning-with-files]`**: 适用于复杂任务的文件式规划系统（Manus-style）
- **`@[executing-plans]`**: 执行已有的实施计划，包含检查点和审查机制
- **`@[using-git-worktrees]`**: 创建隔离的 Git 工作树，用于并行开发或任务切换
- **`@[verification-before-completion]`**: 在声明任务完成前运行验证命令，确保证据确凿
- **`@[using-superpowers]`**: 引导用户发现和使用这些高级技能

### 🧩 系统扩展 (System Extension)
这些技能允许我扩展自身的能力边界。
- **`@[mcp-builder]`**: 构建 MCP (Model Context Protocol) 服务器，连接外部工具和数据
- **`@[skill-creator]`**: 创建新技能或更新现有技能，扩展我的知识库和工作流
- **`@[writing-skills]`**: 辅助编写、编辑和验证技能文件的工具集
- **`@[dispatching-parallel-agents]`**: 分发并行任务给多个 Agent 处理

## 📚 参考文档
- [Anthropic Skills](https://github.com/anthropic/skills)
- [UI/UX Pro Max Skills](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
- [Superpowers](https://github.com/obra/superpowers)
- [Planning with Files](https://github.com/OthmanAdi/planning-with-files)
- [NotebookLM](https://github.com/PleasePrompto/notebooklm-skill)
