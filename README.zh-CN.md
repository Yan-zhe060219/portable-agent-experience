# Portable Agent Experience Kit

[English](README.md) | [简体中文](README.zh-CN.md)

Portable Agent Experience Kit 是一个公开、可安装的 `experience-distiller` Skill。`skills/experience-distiller/` 是本仓库中唯一可安装的对象；适配器仅作为文档提供。它可以帮助 Agent 将一次已完成的成功实践转化为经过隐私审查的候选条目，随后推荐合适的可复用资产类型。

它不是 Agent Memory 产品、MCP 服务器、插件、向量数据库或托管服务。该 Skill 可在兼容的 Agent 之间复用；你真实的经验库则保存在一个独立的私有 Git 仓库中。

## 内容分别存放在哪里

- 本公开仓库包含 Skill、其契约、模板、验证器、适配器以及完全虚构的示例。
- 你的私有仓库包含候选条目以及已验证的 `experiences/`、`workflows/`、`scripts/`、`skills/` 和 `rules/`。
- 原生 Agent Memory 仅作为可选缓存使用。它可以保留一段简短的非敏感摘要，以及资产 ID 和相对路径；它不得成为事实来源，也不得保存完整副本。

## 使用方法

1. 在兼容 Skills 的 Agent 中安装或公开 `skills/experience-distiller/`。
2. 在一次成功对话结束时，显式调用 `experience-distiller`，并提供私有经验仓库的根目录。
3. 审查候选草稿、建议分类、隐私检查结果、证据缺口以及目标相对路径。
4. 在 Skill 写入候选条目前进行批准。仅在记录证据后，才将其晋升为正式资产。

该 Skill 绝不会猜测仓库路径、创建远程仓库、推送内容、安装其他工具，或更改用户级 Agent 设置。

## 验证公开示例

在本仓库根目录中，于 Windows PowerShell、WSL 或 macOS 上运行相同的命令：

```text
python skills/experience-distiller/scripts/validate_library.py examples/sanitized
```

该命令仅使用 Python 标准库；当示例符合已发布的契约时，它将返回 `0`。

## 适配器

- [Codex](adapters/codex.md)
- [Claude Code](adapters/claude-code.md)
- [Cursor](adapters/cursor.md)
- [Copilot](adapters/copilot.md)
- [通用工具框架](adapters/generic-harness.md)

## 安全与发布

请勿在本仓库中放入真实路径、用户名、主机名、私有项目、客户信息、原始对话、机器配置、凭据、Cookie、Token 或 API Key。在作出任何发布决定之前，请检查 `git diff` 并运行验证器。

本框架采用 [MIT](LICENSE) 许可证。该许可证并不授予发布个人经验记录或第三方内容的权利。
