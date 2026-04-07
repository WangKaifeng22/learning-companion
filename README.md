# AI Learning Companion

AI Learning Companion是一个帮助任何人创建定制化AI办学系统的工作流，基于一组可组合的skills和一些可调用OCR阅读PDF或图像的scripts。

## 安装

在你的项目目录中运行以下命令，一键将所有 skills 和辅助脚本安装到项目里：

```bash
npx learning-companion
```

> **手动安装：** 你也可以直接克隆本仓库，将 `skills/` 下的各 `SKILL.md` 复制到你项目的 `.github/copilot/skills/<skill-name>/SKILL.md`，并将 `scripts/` 目录复制到项目根目录。

## 使用方法

创建流程为：1. 建立人物设定 2. 建立交互规则；3. 建立一本/多本文献对应的工作区文件。

你也可以选择跳过某些阶段。

你的 AI 伴学系统创建完成后。每次开始学习时，只需将你希望使用的 AI 模型指向项目文件夹，然后告诉它：

> **"阅读 prompt.txt，然后按照里面的做。"**

每次上课前，编辑 `prompt.txt` 中"今天的微目标是"后面的内容，填入你本次想讨论的具体问题或章节。AI 会自动读取所有配置文件并开始角色扮演教学。

## 文件结构

### Skill 内部结构

```
learning-companion/
├── README.md                          
├── SKILL.md
├── scripts/                            # 工具脚本
│   ├── setup_workspace.py              # 生成工作区文件
│   ├── ocr_caller.py                   # paddleOCR 调用脚本
│   └── mineru_caller.py                # minerU 调用脚本

```

### 生成的伴学项目结构

```
你的项目文件夹/
├── BackgroundAndCharacterSetting.md    # 人物设定（通用，不绑定具体文献）
├── InteractionRules.md                 # 交互规则（通用，不绑定具体文献）
├── scripts/                            # 工具脚本（从 skill 复制过来）
│   ├── setup_workspace.py              # 工作区文件生成脚本
│   ├── ocr_caller.py                   # paddleOCR 调用脚本
│   └── mineru_caller.py                # minerU 调用脚本
└── book_name/                          # 每本文献一个工作区文件夹
    ├── book.(pdf/md/...)               # 要学习的文献
    ├── prompt.txt                      # 每次学习的入口点
    ├── skill_tree.md                   # 已学知识点知识树
    ├── current_focus.md                # 当前进度与下一轮起点
    └── daily_diary.md                  # 每节课的角色视角回顾
```
## 复用同一套人设+规则，换一本书

1. 复制整个配置文件夹，重命名为新的学习项目
2. 编辑 `prompt.txt`，将文献名称替换为新的
3. 清空或保留 `skill_tree.md`、`current_focus.md`、`daily_diary.md`（取决于是否想延续之前的学习记录）
4. 如需调整背景设定中的学习目标，编辑 `BackgroundAndCharacterSetting.md` 中的"当前主线"部分

## 跨项目共享人设

- `BackgroundAndCharacterSetting.md` 和 `InteractionRules.md` 是通用的，不绑定具体文献
- 可以直接复制到新的项目文件夹中使用
- 只需为新项目创建新的 `prompt.txt` 和追踪文件
