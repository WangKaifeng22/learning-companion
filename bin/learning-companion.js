#!/usr/bin/env node

'use strict';

const fs = require('fs');
const path = require('path');

const GREEN = '\x1b[32m';
const CYAN = '\x1b[36m';
const YELLOW = '\x1b[33m';
const RESET = '\x1b[0m';

function log(color, msg) {
  console.log(color + msg + RESET);
}

function copyFile(src, dest) {
  const destDir = path.dirname(dest);
  fs.mkdirSync(destDir, { recursive: true });
  fs.copyFileSync(src, dest);
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      copyFile(srcPath, destPath);
    }
  }
}

function main() {
  const pkgRoot = path.join(__dirname, '..');
  const cwd = process.cwd();

  log(CYAN, '\n🎓 AI Learning Companion — installing skill & scripts\n');

  const installRoot = path.join(cwd, '.github', 'copilot', 'skills', 'learning-companion');

  // Copy SKILL.md → .github/copilot/skills/learning-companion/SKILL.md
  const skillSrc = path.join(pkgRoot, 'SKILL.md');
  const skillDest = path.join(installRoot, 'SKILL.md');
  copyFile(skillSrc, skillDest);
  log(GREEN, '  ✔ skill installed: .github/copilot/skills/learning-companion/SKILL.md');

  // Copy helper scripts → .github/copilot/skills/learning-companion/scripts/
  const scriptsSrc = path.join(pkgRoot, 'scripts');
  const scriptsDest = path.join(installRoot, 'scripts');
  copyDir(scriptsSrc, scriptsDest);
  log(GREEN, '  ✔ scripts installed: .github/copilot/skills/learning-companion/scripts/');

  log(YELLOW, '\n📖 下一步：');
  console.log('  1. 将 AI 模型指向你的项目文件夹');
  console.log('  2. 告诉它："使用 learning-companion skill，帮我创建 AI 伴学系统"');
  console.log('  3. 运行 setup_workspace.py 初始化学习工作区，使用 mineru_caller.py / ocr_caller.py 提取文档内容\n');
}

main();
