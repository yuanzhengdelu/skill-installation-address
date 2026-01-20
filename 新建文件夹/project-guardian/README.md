# 🛡️ Project Guardian 使用说明

## 简介

Project Guardian 帮助 AI 理解并遵守你项目的"隐性规则"，解决两大痛点：
- **交互模式不一致** — 新代码符合项目已有的交互范式
- **修改遗漏关联代码** — 修改时自动检查并同步更新依赖代码

---

## 快速开始

### 第一步：扫描项目

打开终端，运行：

```bash
python "C:\Users\Administrator\.gemini\skills\project-guardian\scripts\scan_project.py" -p "你的项目路径"
```

例如：
```bash
python "C:\Users\Administrator\.gemini\skills\project-guardian\scripts\scan_project.py" -p "E:\MyProject"
```

### 第二步：检查生成的规则

扫描完成后，打开项目中的 `.ai-guardian/` 目录：

```
你的项目/
└── .ai-guardian/
    ├── patterns.md      ← 交互模式规则（检查并修改）
    ├── relations.json   ← 代码依赖关系（自动生成）
    └── user-rules.md    ← 用户自定义规则（添加你的规则）
```

### 第三步：正常开发

从现在开始，AI 在修改你的项目代码时会自动：
1. 读取规则文件
2. 遵守交互模式
3. 检查代码依赖关系

---

## 规则文件说明

### patterns.md — 交互模式

自动识别的交互模式，包括：
- **保存模式**：实时保存、按钮保存、关闭保存
- **输入模式**：下拉菜单、输入框、列表选择

### user-rules.md — 用户规则

你可以添加自定义规则，例如：
```markdown
## 交互规范
- 所有设置页面使用实时保存
- 选项超过5个时使用下拉菜单

## 修改规则
- 修改函数签名时必须同步修改所有调用处
```

### relations.json — 依赖关系

代码依赖关系图（JSON格式），AI 用于检查修改影响范围。

---

## 常见问题

**Q: 规则识别不准确怎么办？**
A: 手动编辑 `patterns.md` 和 `user-rules.md`，明确写出正确的规则。

**Q: 需要重新扫描吗？**
A: 项目结构大变化时可以重新扫描，但 `user-rules.md` 不会被覆盖。

**Q: AI 没有读取规则怎么办？**
A: 在对话中明确说"使用 project-guardian 技能"，或检查规则文件是否在项目根目录。
