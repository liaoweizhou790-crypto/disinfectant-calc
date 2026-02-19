# TOOLS.md - Tool Configuration & Notes

> Document tool-specific configurations, gotchas, and credentials here.

---

## Credentials Location

All credentials stored in `.credentials/` (gitignored):
- `example-api.txt` — Example API key

---

## [Tool Name]

**Status:** ✅ Working | ⚠️ Issues | ❌ Not configured

**Configuration:**
```
Key details about how this tool is configured
```

**Gotchas:**
- Things that don't work as expected
- Workarounds discovered

**Common Operations:**
```bash
# Example command
tool-name --common-flag
```

---

## Android APK Build Workflow

**Status:** ✅ GitHub Actions自动构建

**仓库地址:** https://github.com/liaoweizhou790-crypto/disinfectant-calc

**自动构建触发:**
- 每次推送到 main 分支
- 手动触发 workflow_dispatch

**Artifact命名规范:**
- 使用 ASCII 字符（英文），避免中文下载问题
- 格式: `CDC-Disinfectant-V{版本号}`

**APK下载方法:**
```bash
# 查看最新构建状态
gh run list --repo liaoweizhou790-crypto/disinfectant-calc

# 下载最新APK (替换 RUN_ID)
gh run download RUN_ID --repo liaoweizhou790-crypto/disinfectant-calc --name "CDC-Disinfectant-V1.5.0"
```

**已知问题:**
- Artifact名称含中文字符时，GitHub API下载会返回400错误
- 解决方案：使用英文artifact名称

**文件位置:**
- 构建配置: `.github/workflows/build.yml`
- 输出APK: `app-release-unsigned.apk` (下载后需重命名)

---

## Writing Preferences

[Document any preferences about writing style, voice, etc.]

---

## What Goes Here

- Tool configurations and settings
- Credential locations (not the credentials themselves!)
- Gotchas and workarounds discovered
- Common commands and patterns
- Integration notes

## Why Separate?

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

---

*Add whatever helps you do your job. This is your cheat sheet.*
