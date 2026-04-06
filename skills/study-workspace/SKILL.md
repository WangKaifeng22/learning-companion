---
name: study-workspace
description: Use when a user wants to set up their study workspace — generating prompt.txt, tracking files (skill_tree.md, current_focus.md, daily_diary.md), running cross-checks, and doing a trial run. Includes scripts for OCR and document extraction. Should be used after interaction rules are defined.
---

# Study Workspace

## Overview

This skill generates the study workspace files, validates consistency across all configs, and offers a trial run. It also includes scripts for document extraction (paddleOCR and minerU).

## Prerequisites

- `BackgroundAndCharacterSetting.md` should exist (from companion-setup skill).
- `InteractionRules.md` should exist (from interaction-rules skill).
- If either is missing, inform the user and proceed with available information only.

## Workflow

### Phase 3: Study Workspace Setup

1. **Ask the user** for the name of the literature/textbook they plan to study.

2. **Copy scripts to user project:**
   - Copy the entire `scripts/` directory from this skill's location into the user's project directory.
   - The scripts include:
     - `setup_workspace.py` — generates workspace files from templates
     - `ocr_caller.py` — paddleOCR wrapper for image/PDF text extraction
     - `mineru_caller.py` — minerU wrapper for document conversion
   - After copying, explain that these scripts are now available in their project for future use.

3. **Generate workspace files** using `scripts/setup_workspace.py`:
   ```bash
   python scripts/setup_workspace.py --literature-name "文献名称" --micro-goal "本次学习目标" --output-dir ./项目目录/book_name/
   ```
   This creates:
   - `prompt.txt` — entry point for each study session
   - `skill_tree.md` — knowledge tree of learned concepts
   - `current_focus.md` — current session state
   - `daily_diary.md` — session recap in character voices

4. **Explain to the user** how these files work together:
   - `prompt.txt` is the entry point for each study session
   - `skill_tree.md` accumulates knowledge over time
   - `current_focus.md` tracks where you are and what to do next
   - `daily_diary.md` records session recaps for continuity

5. **Optional: Document extraction tool setup** — Ask the user:

   > "你的文献是否包含扫描件、图片格式的 PDF 或截图？你的 AI 平台是否配置了 paddleOCR 或 minerU 的 API？如果是，我可以在 prompt.txt 中加入调用这些工具的指令，确保 AI 不会直接读取图片而是先提取文本。"

   If the user confirms, proceed with the following:

   **a. Determine which tool the user has:**

   - **minerU** (`mineru-open-api` CLI): No API key needed for `flash-extract` mode. For `extract` mode (higher fidelity, larger files), run `mineru-open-api auth` to set up token. Install: `npm i -g mineru-open-api` or `uv tool install mineru-open-api`.
   - **paddleOCR**: Requires `PADDLEOCR_OCR_API_URL` and `PADDLEOCR_ACCESS_TOKEN` environment variables.
   - **Other OCR tools**: If the user has a different tool, ask for tool name, invocation method, and configuration.

   **b. Help the user configure if not yet done:**
   - For minerU: guide them to run `mineru-open-api auth` (if extract mode needed)
   - For paddleOCR: guide them to set the two environment variables through their platform's config
   - For other tools: ask the user to provide configuration instructions

   **c. Append the appropriate block to `prompt.txt`:**

   **If minerU:**
   ```
   【文档读取规则】
   阅读文献时，如果文件是 PDF、图片或扫描件，请优先调用 minerU 进行文本提取，不要直接读取图片或猜测内容。提取到 Markdown 文本后再进行讲解。
   - 快速阅读/小文件：使用 minerU flash-extract（无需认证，10MB/20页以内）
   - 高精度/大文件/扫描件：使用 minerU extract（需 auth，200MB/600页以内，支持 --ocr）
   - 如果提取失败，告知用户具体错误信息，不要编造内容
   ```

   **If paddleOCR:**
   ```
   【文档读取规则】
   阅读文献时，如果文件是 PDF、图片或扫描件，请优先调用 paddleOCR 的 OCR API 进行文本提取，不要直接读取图片或猜测内容。提取到文本后再进行讲解。
   - 使用脚本 `python scripts/ocr_caller.py --file-path "文件路径" --pretty` 或对应 API 调用方式
   - 如果 API 未配置或调用失败，告知用户具体错误信息，不要编造内容
   ```

   **If other tool:**
   ```
   【文档读取规则】
   阅读文献时，如果文件是 PDF、图片或扫描件，请优先调用 [工具名称] 进行文本提取，不要直接读取图片或猜测内容。提取到文本后再进行讲解。
   - 调用方式：[用户提供的调用命令或步骤]
   - 如果提取失败，告知用户具体错误信息，不要编造内容
   ```

   If the user skipped this step or has no extraction tools, append nothing.

---

### Phase 4: Cross-Check

After all selected phases are done, perform a consistency check:

1. **角色一致性** — Verify that every character mentioned in `InteractionRules.md` has a corresponding entry in `BackgroundAndCharacterSetting.md`.

2. **称呼/口癖一致性** — Verify that catchphrases and speech patterns mentioned in the character settings are reflected in the interaction rules' format guidelines.

3. **结算机制匹配** — If the interaction rules reference output files (`skill_tree.md`, `current_focus.md`, `daily_diary.md`), verify those files were created in Phase 3 (or inform the user they need to create them if Phase 3 was skipped).

4. **难度校准匹配** — Verify that the teaching engine in `InteractionRules.md` reflects the difficulty calibration from Phase 0.5 (scaffolding level, pacing, challenge intensity).

5. **prompt.txt 引用文件存在性** — Verify that `prompt.txt` references files that actually exist on disk.

6. **Report any mismatches** to the user and offer to fix them.

---

### Phase 5: Trial Run

After all phases are complete, offer a trial run:

1. **Ask the user:** "要不要试运行一轮？你可以提供一个简单的微目标，我来模拟 AI 伴学的开场对话，验证人设和规则是否按预期工作。"

2. **If the user agrees:**
   - Read all generated config files
   - Simulate the first turn of a study session based on the user's micro-goal
   - Demonstrate character voices, teaching style, and interaction format
   - Ask the user for feedback: 角色语气对不对？难度合适吗？格式满意吗？

3. **If the user wants changes:** Go back to the relevant phase, iterate, then optionally re-run the trial.

4. **If the user is satisfied:** Proceed to the next step.

---

### Next Step

After all phases are complete, suggest:

> 学习工作区已设置完成。想了解如何导出配置和复用同一套人设换一本书，使用 **export-reuse** skill。也可以直接开始学习，参见项目根目录的 README.md。

---

## Rules

- **Each phase is optional.** Always let the user choose which phases to run.
- **Always wait for user confirmation** before saving files or moving to the next phase.
- **Handle file conflicts:** If a file already exists, ask: "文件 [文件名] 已存在，你想覆盖、另存为新文件、还是合并内容？"
- **Scripts are copied to user project** so that `prompt.txt` can reference them with relative paths.
- **Language matches user.** Follow the user's language preference for all generated content.
