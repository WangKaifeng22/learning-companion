#!/usr/bin/env python3
"""
Study Workspace Setup Script

Generates the four core workspace files for an AI learning companion session:
- prompt.txt
- skill_tree.md
- current_focus.md
- daily_diary.md

Usage:
    python setup_workspace.py --literature-name "文献名称" --micro-goal "本次学习目标" --output-dir ./项目目录/book_name
    python setup_workspace.py --literature-name "文献名称" --output-dir ./项目目录/book_name
    python setup_workspace.py --literature-name "文献名称" --micro-goal "目标" --output-dir ./项目目录/book_name --greeting "自定义问候语"
"""

import argparse
import io
import sys
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


PROMPT_TEMPLATE = """\
阅读InteractionRules.md，然后阅读BackgroundAndCharacterSetting.md和{literature_name}的相关文件（PDF、图片、网页、Word等格式），若有current_focus.md、daily_diary.md和skill_tree.md，也一并阅读。【如果你完全理解了，请详细阐述我的要求。在这之后，说"{greeting}"并开始今天的角色扮演。】今天的微目标是：{micro_goal}
"""

SKILL_TREE_TEMPLATE = """\
# 知识树 / Skill Tree

## [章节/模块名称]
- [概念]: [定义与核心逻辑]
"""

CURRENT_FOCUS_TEMPLATE = """\
# Current Focus

- **今日梗概**：
- **下一轮精确起点**：
- **当前误区/卡壳点**：
- **内部梗/教学策略**：
"""

DAILY_DIARY_TEMPLATE = """\
# Daily Diary

## {date}
- [角色视角的课程回顾]
"""


def create_file(path: Path, content: str, label: str):
    if path.exists():
        print(f"[WARN] {label} already exists at {path}, skipping.", file=sys.stderr)
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[OK] Created {label}: {path}", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate study workspace files for AI learning companion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_workspace.py --literature-name "国家与革命" --micro-goal "理解第一章核心论点" --output-dir ./国家与革命
  python setup_workspace.py --literature-name "湖南农民运动考察报告" --output-dir ./湖南农民运动考察报告 --greeting "好的，我们开始吧"
        """,
    )
    parser.add_argument(
        "--literature-name",
        required=True,
        help="Name of the literature/textbook to study",
    )
    parser.add_argument(
        "--micro-goal",
        default="[用户填写本次学习的具体目标或问题]",
        help="Today's micro-goal (default: placeholder)",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Output directory for workspace files (default: current directory)",
    )
    parser.add_argument(
        "--greeting",
        default="是的，主人，我们开始上课吧",
        help="Custom greeting phrase for the AI (default: 是的，主人，我们开始上课吧)",
    )

    args = parser.parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()

    today = datetime.now().strftime("%Y-%m-%d")

    files_created = 0

    # prompt.txt
    prompt_content = PROMPT_TEMPLATE.format(
        literature_name=args.literature_name,
        micro_goal=args.micro_goal,
        greeting=args.greeting,
    )
    if create_file(output_dir / "prompt.txt", prompt_content, "prompt.txt"):
        files_created += 1

    # skill_tree.md
    if create_file(output_dir / "skill_tree.md", SKILL_TREE_TEMPLATE, "skill_tree.md"):
        files_created += 1

    # current_focus.md
    if create_file(output_dir / "current_focus.md", CURRENT_FOCUS_TEMPLATE, "current_focus.md"):
        files_created += 1

    # daily_diary.md
    diary_content = DAILY_DIARY_TEMPLATE.format(date=today)
    if create_file(output_dir / "daily_diary.md", diary_content, "daily_diary.md"):
        files_created += 1

    if files_created == 0:
        print("No new files created (all already exist).", file=sys.stderr)
        sys.exit(0)

    print(f"\nWorkspace setup complete: {files_created}/4 files created in {output_dir}", file=sys.stderr)
    print(f"\nNext step: Edit prompt.txt to set today's micro-goal before each session.", file=sys.stderr)


if __name__ == "__main__":
    main()
