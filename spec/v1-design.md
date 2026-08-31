# Portable Agent Experience Kit：v1 设计规格（审核后修订稿）

**状态：** 已获方向批准；可据此进入实施规划。  
**目标：** 交付一个可公开发布、可安装到不同 Agent 的 `experience-distiller` Skill。该 Skill 在会话结束时协助用户把成功经历沉淀到一个由用户指定的**独立私有 Git 经验仓库**；经验仓库是事实真源。

## 1. 已确认的边界

- 公开项目交付的是可安装的 Skill 及其通用资源；它不保存真实个人经验。
- 私有经验仓库使用 Git 管理的 Markdown/YAML 文件，独立于 Codex、Claude、DeepSeek、Cursor、向量数据库和厂商 API。
- 用户安装 Skill 后，在首次使用时或每次调用时指定经验仓库位置；Skill 只在该位置沉淀和检索经验。
- Agent 原生 Memory 只可作为可选的短缓存或索引指针，绝不复制完整经验库，也不是事实真源。
- DeepSeek 在 Codex/OpenCodex 内运行时复用同一个已安装 Skill；独立 harness 通过适配说明调用同一套方法。
- MCP、插件、远程服务、向量检索和自动同步均不属于 v1。
- 未来脚本只使用 Python 标准库，支持 Windows、WSL 和 macOS；不引入第三方依赖。
- 公开内容不得包含真实路径、个人经验、机器配置、凭据或私有 Agent 配置。

## 2. 当前项目基线

2026-08-31 的盘点结果：工作目录原本为空；尚未初始化 Git；未发现项目级 `AGENTS.md`。本设计阶段只创建和修订本文件，不包含远程仓库、推送、发布、全局安装或用户级配置修改。

## 3. 组织方案比较

### 方案 A：可安装 Skill + 独立私有经验仓库（推荐）

公开仓库的主产品是一个自包含 Skill 目录。它内含方法、数据契约、模板和标准库校验脚本；用户将它安装到支持 Skill 的 Agent。真实候选卡和成熟资产位于用户指定的私有 Git 仓库。

优点：Skill 是可跨 Agent 分发的操作入口，经验是可私密、可迁移的长期资产；公开框架无需镜像或携带任何真实内容。缺点：首次使用需要安装 Skill 并指定私有仓库路径。

### 方案 B：公开仓库内置 `experience/` 作为主要库

在公开项目中保留一个可直接写入的经验目录，真实内容依靠约定不提交。

优点：新用户可以立刻试用。缺点：真实经验与公开框架混在同一工作树，误提交和误发布风险高；也不符合“独立私人仓库”的使用模型。

### 方案 C：按 Agent 维护多份完整 Skill 与经验库

每个 Agent 有自身的 Skill 副本、经验副本和工作流副本。

优点：各环境的入口看似直接。缺点：内容漂移、重复维护，且模型与 harness 会被错误绑定；不符合可移植性目标。

**结论：** 采用方案 A。公开 Skill 负责能力和流程，私有 Git 仓库负责知识和证据；两者通过稳定的数据契约连接。

## 4. 两个仓库的最小结构

### 4.1 公开：Portable Agent Experience Kit

以一个可独立安装的 Skill 文件夹为中心，借鉴开放 Agent Skills 约定：`SKILL.md` 是入口，可携带脚本、模板和参考资料。

```text
portable-agent-experience/
├── README.md                         # 安装、指定私有库、调用与安全边界
├── LICENSE                           # MIT
├── AGENTS.md                         # 公开仓库协作与脱敏规则
├── skills/
│   └── experience-distiller/
│       ├── SKILL.md                  # 唯一入口：末尾复盘、检索、分类、审批提示
│       ├── references/
│       │   ├── card-contract.md      # Markdown/YAML 数据契约
│       │   ├── classification.md     # 候选卡的明确分类判定表
│       │   └── portability.md        # 隐私与跨平台要求
│       ├── templates/
│       │   └── candidate-card.md     # 先创建候选卡的模板
│       └── scripts/
│           └── validate_library.py   # 仅标准库的结构/隐私启发式校验
├── adapters/
│   ├── codex.md
│   ├── claude-code.md
│   ├── cursor.md
│   ├── copilot.md
│   └── generic-harness.md            # 无 Skill harness 的最小调用包装
├── examples/
│   └── sanitized/                    # 虚构的候选卡与分类示例
├── tests/
│   └── fixtures/                     # 可通过与应失败的脱敏样本
└── spec/
    └── v1-design.md                  # 本设计文档
```

`references/`、`templates/` 与 `scripts/` 随 `experience-distiller` 一起安装；公开仓库根目录的 `adapters/` 仅解决发现和调用差异，不复制 Skill 逻辑。`workflows/`、`experience/`、`rules/` 等不是公开框架的顶级目录，而属于私有经验仓库的分类结果。

### 4.2 私有：用户经验仓库

用户自行创建并指定该仓库位置。Skill 在每次拟写前确认它是私有目标；仓库内不需要安装任何厂商插件。

```text
my-agent-experience/                  # 独立、私有、Git 管理
├── candidates/                       # 未被批准的候选卡
├── experiences/                      # 已验证的可复用结论
├── workflows/                        # 多步骤、人工可执行的流程
├── scripts/                          # 可运行且已验证的自动化
├── skills/                           # 从经验升格出的专用可安装 Skill
└── rules/                            # 可引入项目 AGENTS 指令的稳定规则
```

原生 Memory 不在上述目录中：它是可丢弃缓存。若使用，Skill 只生成不含敏感数据的短摘要和来源 `id`/相对路径，绝不把一张完整卡复制进去。

## 5. 候选卡数据契约

候选卡是 UTF-8 Markdown，开头为 YAML front matter。YAML 提供机器校验和纯文本筛选所需的稳定字段，正文保留可审查的上下文和证据。

```yaml
schema_version: "1.0"
id: "cand-portable-python-paths"
title: "Use platform-neutral Python paths in repository scripts"
status: "candidate"                  # candidate | approved | verified | deprecated | superseded
summary: "Short, non-sensitive reusable conclusion or hypothesis."
tags: ["python", "portability"]
platforms: ["windows", "wsl", "macos"]
created: "2026-08-31"
updated: "2026-08-31"
privacy: "private"                   # public-sanitized | private
proposed_kind: "script"              # experience | workflow | script | skill | agents_rule | memory_cache
evidence: []
```

必填字段为 `schema_version`、`id`、`title`、`status`、`summary`、`tags`、`platforms`、`created`、`updated`、`privacy`、`proposed_kind` 和 `evidence`。`id` 必须在私有仓库内唯一，使用小写 kebab-case，且改名不改变 `id`。

正文固定区段为：`## Context`、`## Observation`、`## Reusable guidance`、`## Validation`、`## Risks and rollback`、`## Sanitization notes`。候选卡必须说明还缺什么证据；在获批和验证前不可改变 Agent 默认行为。

成熟资产保留同一套核心字段，并新增：

```yaml
kind: "script"
status: "verified"
derived_from: ["cand-portable-python-paths"]
```

## 6. 分类建议：候选卡应变成什么

Skill 在生成候选卡后必须给出一个 `proposed_kind`、理由、所需证据和备选项。分类以**最终消费方式**为准，而非由哪个 Agent 产生。

| 类别 | 应选择它的条件 | 必须补足的内容 | 不应选择它的情形 |
| --- | --- | --- | --- |
| `experience` | 结论可复用，但不需要固定步骤或自动化 | 可复查证据、适用/不适用边界 | 只是单次观察或可精确自动化 |
| `workflow` | 人需要按顺序执行多个步骤，且存在判断点或审批点 | 前置条件、步骤、分支、检查点、回滚 | 只是一条规则或确定性命令 |
| `script` | 输入/输出可定义，重复执行能显著降低出错，且可用代码验证 | 标准库源码、运行方式、正/负 fixture、预期输出 | 需要大量人工判断或依赖私有环境 |
| `skill` | 需要 Agent 按一套可复用方法完成多步推理、检索或产出，且会跨会话/项目使用 | `SKILL.md`、范围、输入输出、引用资源、示例 | 仅是一次性 Prompt 或单条事实 |
| `agents_rule` | 是稳定、高频、简短、可执行的项目协作约束 | 规则文本、适用范围、来源卡、冲突处理 | 复杂流程、偏好或尚未验证的做法 |
| `memory_cache` | 仅需让特定 Agent 快速记住一条低敏感短提醒 | 不超过简短摘要、来源 `id` 和相对路径；可安全丢失 | 任何完整经验、步骤、证据或敏感信息 |

`memory_cache` 不是私有库中的独立事实资产。它总是从 `experience`、`workflow`、`script`、`skill` 或 `agents_rule` 派生，且失效或删除时不影响私有库内容。

## 7. 审批、验证与升格流程

```text
会话结束的成功经历
  → Candidate（记录假设、隐私检查、建议分类、待补证据）
  → 人工审批（确认可保留、脱敏、分类合理）
  → 验证（复现/测试/人工复核，记录 evidence）
  → 选择一个主分类：experience | workflow | script | skill | agents_rule
  ↘ 可选：生成 memory_cache（仅摘要 + 来源指针）
```

1. 用户在对话末尾显式调用 Skill；Skill 询问或读取本次指定的私有经验仓库位置，并先做只读检索、去重和敏感信息筛查。
2. Skill 先展示候选卡草案、建议分类、证据缺口和拟写入的相对路径，等待用户审批后才写入 `candidates/`。
3. 审批通过表示“值得保留且可安全写入私有库”；它不等于结论已验证。
4. 验证证据充分时，将卡移动或重写为主分类目录中的已验证资产，并写入 `kind`、`status: verified` 和 `derived_from`。
5. 升格后的每一项都须回链候选卡；被弃用项目保留 `deprecated` 或 `superseded` 状态与替代引用，不静默删除。
6. 若用户要求 Memory 缓存，Skill 仅在主分类已验证后提出一条可选缓存文本；写入具体 Agent 的 Memory 仍由适配器、用户权限和该环境能力决定。

## 8. Skill 使用模型与适配器

安装后，用户为 Skill 指定一个私有经验仓库根。例如，在会话结束时请求“使用 experience-distiller，将本次成功经验沉淀到已指定的私有经验库”。若没有已指定位置，Skill 必须先询问，不能猜测路径或扫描用户机器。

核心 Skill 的职责：定位指定库；读取本 Skill 的 references；进行隐私筛查、全文检索、候选生成、分类建议、审批提示和验证/升格建议；所有写入前展示变更。它不保存真实经验，不绑定模型，也不安装/修改任何 Agent 配置。

最小适配器只记录以下内容：如何安装/发现该 Skill，如何向它传入私有库位置，怎样在该 Agent 中显式调用，以及原生 Memory 的可选、仅指针缓存策略。

| 环境 | v1 最小适配方式 |
| --- | --- |
| Codex | 安装公开 Skill；通过项目/会话上下文提供私有库位置并显式调用 |
| Claude Code | 安装或映射同一 Skill；以项目指令或命令传入私有库位置 |
| Cursor | 通过项目规则或用户可用的 Skill 入口调用，不复制经验库 |
| Copilot | 通过仓库指令或提示入口调用相同方法，不要求插件 |
| 通用 harness | 读取 `SKILL.md` 和 references，并把私有库根作为显式参数传入 |

## 9. 隐私、验证和迁移

公开仓库只允许框架、规则、脚本源码、虚构样例和测试 fixture。禁止真实绝对路径、用户名、主机名、项目/客户信息、真实对话、个人经验、机器配置、凭据及其可还原变体。MIT 许可证仅覆盖本公开框架，不改变私有经验或第三方内容的权利状态。

结构校验器检查 front matter、枚举、日期、唯一 `id`、正文区段和 `derived_from`。隐私启发式只检测公开样例中的常见敏感模式，不能代替人工审查。跨平台验证应在 Windows PowerShell、WSL shell 和 macOS shell 使用各自 `python` 运行同一标准库脚本；不得依赖 shell 专属语法、硬编码路径或第三方包。

迁移时：安装公开 Skill；创建/选择私有 Git 经验库；显式提供库位置；运行校验；再按适配器决定是否写入一条可丢弃的缓存指针。丢失任何原生 Memory 后，必须仍能从私有 Git 库完整恢复。

## 10. v1 验收标准与排除项

验收标准：

- `experience-distiller` 可作为单独目录安装，并携带其所需的引用、模板和标准库脚本。
- 用户能够在对话结束时显式调用 Skill，并指定私有经验仓库，而公开项目中不会出现真实经验。
- 一张脱敏候选卡能得到清晰的分类建议、审批提示和验证/升格路径；六类分类可被区分。
- fixture 至少包含一个应通过和一个应失败的案例，校验脚本能区分它们。
- Codex、Claude Code、Cursor、Copilot 与通用 harness 都有最小接入说明；它们不依赖厂商云服务或复制事实库。

v1 排除远程仓库创建、推送、发布、用户级配置自动修改、自动安装、MCP、插件、向量数据库、厂商 API、真实个人经验和自动同步 Memory。

