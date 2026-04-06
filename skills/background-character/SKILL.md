---
name: background-character
description: Use when a user wants to create or edit a customized AI learning companion — defining character personas, interaction rules, and study workspace through an iterative conversation. This is the entry-point skill that covers scope selection, difficulty calibration, and character persona creation.
---

# Companion Setup

## Overview

A guided, iterative workflow that helps users create or edit a complete AI learning companion setup. This skill covers scope selection, difficulty calibration, and character persona creation.

## Workflow

### Phase 0: Scope Selection

**First, check if existing config files exist** in the user's project directory (`BackgroundAndCharacterSetting.md`, `InteractionRules.md`, `prompt.txt`, etc.).

- **If files exist:** Ask the user whether they want to **edit existing config** or **create from scratch**.
  - Edit: Read existing files, let the user specify what to change, iterate, then save.
  - Create from scratch: proceed with the full workflow below.

- **If no files exist:** Present the three phases:
  1. **人物设定** — 创建伴学角色的背景和人设
  2. **交互规则** — 定义教学方式和对话规则
  3. **学习工作区** — 生成 prompt.txt 和追踪文件

  用户可以全选，也可以只选其中任意一个或多个。跳过的阶段直接省略。

---

### Phase 0.5: Difficulty / Knowledge Calibration

Before drafting personas or rules, calibrate to the user's level. Ask:

1. **知识基础：** 用户对当前要学的主题了解多少？（零基础 / 有初步了解 / 已入门想深入 / 进阶）
2. **期望难度：** 希望 AI 提问和讲解的难度？（循序渐进、多引导 / 中等、适当挑战 / 高强度、直接深入）
3. **学习节奏：** 偏好快还是慢？（快速过核心概念 / 逐字逐句精读 / 灵活调整）

Use the answers to:
- Adjust the **teaching engine** in Phase 2 (more scaffolding vs. more direct challenge)
- Adjust the **character behavior** in Phase 1 (e.g., a character might simplify explanations for beginners, or dive into proofs for advanced users)
- Set the **default session pace** in the interaction rules

---

### Phase 1: Character Persona Creation

1. **Ask the user** what fictional/real person (or group of people) they want to base their learning companion(s) on.

2. **Ask the user** how many companions they want (1-on-1, 2 companions, 3+, etc.). This affects the interaction dynamics drafted later.

3. **Ask the user** whether they want to write the detailed character settings themselves or have you draft them.

4. **If the user writes their own:**
   - Read their draft
   - Provide concrete suggestions for improvement across these dimensions:
     - Identity and motivation (who they are, why they are here)
     - Academic/learning style (how they approach problems)
     - Interaction traits (catchphrases, 称呼, personality quirks)
     - Complementary dynamics between multiple characters (if more than one)
   - Iterate with the user until they are satisfied

5. **If you draft:**
   - Ask the user for key traits they want (personality, expertise, quirks)
   - Generate a draft following this structure:
     ```
     # 学习小组背景与人物设定

     ## 背景设定
     1. [Overall setting: who, where, relationship]
     2. [Current learning goal/project]

     ## 人物设定

     ### 1. [角色名]
     * **身份与动机：** [who they are, why they participate]
     * **学术风格：** [how they learn/teach, strengths, analogies they use]
     * **互动特征：** [catchphrases, 称呼, personality in dialogue]
     ```
   - Iterate with the user until satisfied

6. **Save** the final version as `BackgroundAndCharacterSetting.md` in the user's project directory.

---

### Next Step

After Phase 1 is complete, suggest:

> 人物设定已完成。下一步是创建交互规则，定义教学方式和对话规则。使用 **interaction-rules** skill 继续。

---

## Rules

- **Each phase is optional.** Always let the user choose which phases to run.
- **Check for existing files first.** If config files already exist, offer to edit instead of recreate.
- **Always wait for user confirmation** before saving files or moving to the next phase.
- **Handle file conflicts:** If a file the user wants to create already exists, ask: "文件 [文件名] 已存在，你想覆盖、另存为新文件、还是合并内容？"
- **Adapt, don't copy.** The character settings should feel unique to the user's chosen characters, not generic templates.
- **Respect user preferences.** If the user wants minimal characters or custom formats, accommodate them.
- **Language matches user.** If the user communicates in Chinese, use Chinese for all generated content. If English, use English. Follow the user's lead.
