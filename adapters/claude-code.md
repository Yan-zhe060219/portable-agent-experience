# Claude Code 适配器

## Skill discovery

通过项目指令或命令入口发现并映射公开的 `skills/experience-distiller/`。它是唯一需要安装或映射的对象；本适配器仅提供接入说明。

不要安装 MCP 或插件，也不要把私有经验库复制到当前公开仓库、Skill 目录或其他事实存储。

## Private repository input

仅在用户明确提供私有经验库根时使用该根。例如，可在命令入口中传入：

```text
<private-experience-repo>
```

不得猜测、扫描或持久化该位置；私有库仍是唯一事实来源。

## End-of-conversation invocation

成功完成会话后，用户从项目指令或命令入口显式调用 `experience-distiller`，并同时提供私有库根：

```text
experience-distiller <private-experience-repo>
```

Skill 会先进行只读检索、脱敏和候选草案展示；未经明确批准，不写入候选或升格资产。

## Optional memory cache

Memory 仅可选地保存低敏感摘要及已验证主资产的相对来源指针。不得复制事实库、完整候选或经验正文；未经明确批准不得写入 Memory。
