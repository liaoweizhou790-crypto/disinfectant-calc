# 待办事项：多代理路由配置

> 创建时间：2026-02-19
> 优先级：高

---

## 当前状态
- ✅ 1 个 Agent（main）处理所有任务
- ⏳ 需要拆分为多个独立 Agent

---

## 待办清单

### 🔴 高优先级
- [ ] 1. 创建 `cdc` Agent（疾控业务）
  - 命令：`openclaw agents add cdc`
  - 复制 `SOUL.md`, `USER.md`, `AGENTS.md`
  
- [ ] 2. 配置 `~/.openclaw/openclaw.json` 多代理路由
  - main → webchat
  - cdc → feishu（工作号）
  
- [ ] 3. 重启 Gateway 测试路由

### 🟡 中优先级
- [ ] 4. 创建 `dev` Agent（开发工作）
- [ ] 5. 配置 Telegram 渠道 → dev Agent
- [ ] 6. 迁移消毒剂计算器项目到 cdc Agent 工作空间

### 🟢 低优先级
- [ ] 7. 配置群组 @提及切换规则
- [ ] 8. Agent 间通信测试

---

## 快速命令备忘

```bash
# 添加 Agent
openclaw agents add cdc

# 查看列表
openclaw agents list --bindings

# 连接指定 Agent
openclaw tui --agent cdc

# 重启 Gateway
openclaw gateway restart
```

---

## 配置文件模板

位置：`~/.openclaw/openclaw.json`

```json5
{
  agents: {
    list: [
      { id: "main", default: true, workspace: "~/.openclaw/workspace" },
      { id: "cdc", workspace: "~/.openclaw/workspace-cdc" },
      { id: "dev", workspace: "~/.openclaw/workspace-dev" }
    ]
  },
  bindings: [
    { agentId: "main", match: { channel: "webchat" } },
    { agentId: "cdc", match: { channel: "feishu" } }
  ]
}
```
