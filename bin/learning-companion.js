#!/usr/bin/env node

'use strict';

const fs = require('fs');
const path = require('path');

const SKILLS = ['background-character', 'interaction-rules', 'study-workspace'];

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

  log(CYAN, '\n🎓 AI Learning Companion — installing skills\n');

  // Install everything under .github/copilot/skills/learning-companion/
  const installRoot = path.join(cwd, '.github', 'copilot', 'skills', 'learning-companion');

  // Copy skill files → .github/copilot/skills/learning-companion/skills/<name>/SKILL.md
  const skillsSrc = path.join(pkgRoot, 'skills');
  for (const skill of SKILLS) {
    const src = path.join(skillsSrc, skill, 'SKILL.md');
    const dest = path.join(installRoot, 'skills', skill, 'SKILL.md');
    copyFile(src, dest);
    log(GREEN, `  ✔ skill installed: .github/copilot/skills/learning-companion/skills/${skill}/SKILL.md`);
  }

  // Copy helper scripts → .github/copilot/skills/learning-companion/scripts/
  const scriptsSrc = path.join(pkgRoot, 'scripts');
  const scriptsDest = path.join(installRoot, 'scripts');
  copyDir(scriptsSrc, scriptsDest);
  log(GREEN, '  ✔ scripts installed: .github/copilot/skills/learning-companion/scripts/');

  log(YELLOW, '\n📖 下一步：');
  console.log('  1. 将 AI 模型指向你的项目文件夹');
  console.log('  2. 告诉它："使用 background-character skill，帮我创建 AI 伴学系统"');
  console.log('  3. 按照引导依次完成 background-character → interaction-rules → study-workspace\n');
}

main();
