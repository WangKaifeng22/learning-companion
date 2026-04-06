---
name: export-reuse
description: Use when a user wants to export their AI learning companion configuration, reuse the same persona and rules for a new book, or share configurations across projects.
---

# Export and Reuse

## Overview

This skill guides users through exporting, reusing, and sharing their AI learning companion configurations across projects.

## Workflow

### Reuse Same Setup for a New Book

1. Copy the entire configuration folder and rename it for the new study project.
2. Edit `prompt.txt`, replacing the literature name with the new one.
3. Choose whether to clear or keep `skill_tree.md`, `current_focus.md`, and `daily_diary.md` (depending on whether to continue previous learning records).
4. If needed, edit `BackgroundAndCharacterSetting.md` to update the "current learning goal" section.

### Cross-Project Persona Sharing

- `BackgroundAndCharacterSetting.md` and `InteractionRules.md` are generic and not tied to any specific literature.
- They can be directly copied into new project folders.
- Only a new `prompt.txt` and tracking files need to be created for each project.

### Export Configuration

- Package the entire folder (zip/tar) for a complete export.
- This includes all configuration files and existing learning records.

---

## Rules

- **Language matches user.** Follow the user's language preference for all generated content.
- **Preserve file integrity.** When copying configurations, ensure all referenced files exist in the new location.
