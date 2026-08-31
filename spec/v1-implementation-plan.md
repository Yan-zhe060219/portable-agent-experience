# Portable Agent Experience Kit v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建可安装的 `experience-distiller` Skill，使其能把经用户审批的候选经验写入一个显式指定的私有 Git 经验仓库，并给出可验证的分类、隐私和跨平台保障。

**Architecture:** 公开仓库只分发一个自包含 Skill 目录，其 references、模板和校验脚本随 Skill 一起使用。Skill 不保存真实经验；它将一个用户明确提供的私有仓库根作为唯一事实源，先生成候选卡，再依据分类规则升格为经验、Workflow、Script、Skill 或 AGENTS 规则，并可选生成仅含指针的 Memory 缓存建议。

**Tech Stack:** Markdown、YAML front matter 的受限子集、Python 3 标准库、`unittest`、Git（仅本地初始化；提交另需授权）。

---

## 文件结构与职责

```text
README.md                                      # 公开项目定位、安装和私有库使用
LICENSE                                        # MIT 正文
AGENTS.md                                      # 公开仓库的协作/脱敏规则
skills/experience-distiller/SKILL.md           # 可安装 Skill 的主指令
skills/experience-distiller/references/*.md    # 契约、分类、可移植性规范
skills/experience-distiller/templates/*.md     # 候选卡模板
skills/experience-distiller/scripts/*.py       # 标准库校验命令
adapters/*.md                                  # 五种环境的最小接入说明
examples/sanitized/*.md                        # 仅虚构、公开安全的分类演示
tests/fixtures/{valid,invalid}/*.md            # 校验器的输入样本
tests/test_validate_library.py                  # 校验器单元和命令行测试
spec/v1-design.md                              # 已审核设计
```

私有经验仓库不是本项目的子目录；其约定目录为 `candidates/`、`experiences/`、`workflows/`、`scripts/`、`skills/` 与 `rules/`。任何 `memory_cache` 都是可选外部缓存，不在公开仓库或私有事实库中保存完整副本。

### Task 1: 建立本地仓库骨架与公开边界

**Files:**

- Create: `README.md`
- Create: `LICENSE`
- Create: `AGENTS.md`
- Create: `.gitignore`

- [ ] **Step 1: 初始化本地 Git（仅此处获得用户批准）**

Run: `git init`

Expected: 输出 `Initialized empty Git repository`，且不创建远程地址、不提交、不推送。

- [ ] **Step 2: 写入 MIT 许可证完整文本**

使用 SPDX 标识 `MIT`，版权年份与署名位置留给仓库所有者在发布前填写；不得复制任何第三方仓库的许可证文本或声明其为本项目许可。

- [ ] **Step 3: 写入公开 README**

README 必须包含：项目不是 Memory/MCP/插件服务；Skill 是可安装载体；真实内容位于独立私有 Git 仓库；首次调用需显式指定私有库根；候选→审批→验证→分类流程；不自动安装、不写用户级配置、不创建远程仓库的安全声明；以及指向五个适配器的链接。

- [ ] **Step 4: 写入根 `AGENTS.md` 与 `.gitignore`**

`AGENTS.md` 明确禁止提交真实经验、真实路径、机器配置、凭据和私有配置；要求写入私有库前展示拟变更，且未经明确授权不得进行远程/Git 提交操作。`.gitignore` 忽略 `.env`、`*.pem`、`*.key`、Python 缓存和本地编辑器文件，但不得忽略 `examples/` 或 `tests/fixtures/`。

- [ ] **Step 5: 检查公开边界文件**

Run: `rg -n -i 'token|api[ _-]?key|password|secret|C:\\Users|/home/' README.md AGENTS.md .gitignore`

Expected: 只有脱敏规则文字可能匹配；不得出现真实值或真实个人路径。

### Task 2: 编写受限卡片契约、分类规则和候选模板

**Files:**

- Create: `skills/experience-distiller/references/card-contract.md`
- Create: `skills/experience-distiller/references/classification.md`
- Create: `skills/experience-distiller/references/portability.md`
- Create: `skills/experience-distiller/templates/candidate-card.md`
- Create: `examples/sanitized/candidate-script-example.md`
- Create: `examples/sanitized/workflow-example.md`

- [ ] **Step 1: 定义机器可校验的 YAML 子集**

在 `card-contract.md` 规定 front matter 被 `---` 包围；顶层只接受 `key: scalar`、JSON 风格字符串数组和 `evidence: []`。必填键为：`schema_version`、`id`、`title`、`status`、`summary`、`tags`、`platforms`、`created`、`updated`、`privacy`、`proposed_kind`、`evidence`。这样校验器能仅使用标准库 `json` 和字符串解析，而不需要 PyYAML。

- [ ] **Step 2: 定义枚举和不变量**

契约中固定：`status` 为 `candidate|approved|verified|deprecated|superseded`；`privacy` 为 `private|public-sanitized`；`proposed_kind` 和成熟资产 `kind` 为 `experience|workflow|script|skill|agents_rule|memory_cache`。`id` 使用 `^[a-z][a-z0-9-]*$`；日期为 ISO `YYYY-MM-DD`；正文必须按设计规格拥有六个二级标题；`memory_cache` 只能引用已验证主资产且不得包含完整正文。

- [ ] **Step 3: 写入分类判定表和决策顺序**

`classification.md` 逐项包含“选择条件、必需证据、不适用条件”：

1. 可复用结论但不需要步骤 → `experience`。
2. 多步骤且包含判断/审批点 → `workflow`。
3. 输入输出可定义、重复执行能降低错误 → `script`。
4. Agent 需跨会话按方法完成多步工作 → `skill`。
5. 稳定、高频、短而可执行的协作约束 → `agents_rule`。
6. 仅低敏感的短提醒 → `memory_cache`，并作为已验证主资产的可丢弃派生物。

- [ ] **Step 4: 写入模板与脱敏样例**

模板使用虚构 `cand-` 前缀、空 `evidence`、六个正文区段，并要求“证据缺口”和“推荐分类理由”。两个样例分别演示候选 Script 与已验证 Workflow，使用相对路径和虚构内容，不使用任何真实机器信息。

- [ ] **Step 5: 人工规格检查**

Run: `rg -n 'schema_version|proposed_kind|memory_cache|## Context|## Sanitization notes' skills/experience-distiller/references skills/experience-distiller/templates examples/sanitized`

Expected: 三份 reference、模板和两个样例都能展示其需要的契约/分类或正文区段。

### Task 3: 先写校验器失败测试和 fixture

**Files:**

- Create: `tests/fixtures/valid/candidate-script.md`
- Create: `tests/fixtures/invalid/missing-proposed-kind.md`
- Create: `tests/fixtures/invalid/invalid-id.md`
- Create: `tests/fixtures/invalid/missing-section.md`
- Create: `tests/test_validate_library.py`

- [ ] **Step 1: 创建 fixture**

有效 fixture 使用全部必填键、`proposed_kind: script` 和六个要求区段。三个无效 fixture 分别删除 `proposed_kind`、使用 `Bad_ID`、删除 `## Risks and rollback`。所有 fixture 使用 `privacy: public-sanitized` 和虚构文本。

- [ ] **Step 2: 写入失败测试**

```python
from pathlib import Path
import unittest

from validate_library import validate_file

FIXTURES = Path(__file__).parent / "fixtures"

class ValidateLibraryTests(unittest.TestCase):
    def test_accepts_valid_candidate(self):
        self.assertEqual([], validate_file(FIXTURES / "valid" / "candidate-script.md"))

    def test_rejects_missing_proposed_kind(self):
        errors = validate_file(FIXTURES / "invalid" / "missing-proposed-kind.md")
        self.assertIn("missing required key: proposed_kind", errors)

    def test_rejects_invalid_id(self):
        errors = validate_file(FIXTURES / "invalid" / "invalid-id.md")
        self.assertIn("invalid id", errors)

    def test_rejects_missing_required_section(self):
        errors = validate_file(FIXTURES / "invalid" / "missing-section.md")
        self.assertIn("missing section: ## Risks and rollback", errors)
```

- [ ] **Step 3: 运行测试以确认失败**

Run: `python -m unittest tests.test_validate_library -v`

Expected: FAIL，原因是 `validate_library` 尚不存在；不要在此步骤安装测试框架。

### Task 4: 实现标准库校验器并使测试通过

**Files:**

- Create: `skills/experience-distiller/scripts/validate_library.py`
- Modify: `tests/test_validate_library.py`

- [ ] **Step 1: 定义公共函数和受限 front matter 解析器**

```python
def validate_file(path: Path) -> list[str]:
    """Return all contract errors for one UTF-8 Markdown experience card."""

def validate_tree(root: Path) -> dict[Path, list[str]]:
    """Validate every Markdown card below root and detect duplicate ids."""

def main(argv: list[str] | None = None) -> int:
    """Print one error per file and return 0 only when all files are valid."""
```

实现仅用 `argparse`、`datetime`、`json`、`pathlib`、`re` 和 `sys`。解析器拒绝不含起始/结束 `---` 的文件、重复键、未识别的复杂 YAML 值；把 JSON 风格数组用 `json.loads` 解析。`validate_file` 按 Task 2 的键、枚举、日期、ID、正文标题和 `memory_cache` 限制累积错误，不在首个错误处退出。

- [ ] **Step 2: 增加命令行测试**

在 `tests/test_validate_library.py` 新增：

```python
import subprocess
import sys

def test_command_returns_nonzero_for_invalid_tree(self):
    script = Path(__file__).parents[1] / "skills" / "experience-distiller" / "scripts" / "validate_library.py"
    result = subprocess.run(
        [sys.executable, str(script), str(FIXTURES / "invalid")],
        capture_output=True, text=True, check=False,
    )
    self.assertEqual(1, result.returncode)
    self.assertIn("missing required key: proposed_kind", result.stdout)
```

在测试模块顶部加入：

```python
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "skills" / "experience-distiller" / "scripts"))
```

- [ ] **Step 3: 运行单元测试**

Run: `python -m unittest tests.test_validate_library -v`

Expected: 所有四个契约测试和一个命令行测试均为 `ok`。

- [ ] **Step 4: 运行公开样例校验**

Run: `python skills/experience-distiller/scripts/validate_library.py examples/sanitized`

Expected: 返回码 `0`，不输出错误行。

### Task 5: 编写可安装的 `experience-distiller` 主指令

**Files:**

- Create: `skills/experience-distiller/SKILL.md`

- [ ] **Step 1: 写入 Skill 元数据和资源定位方式**

在开头写 YAML front matter：

```yaml
---
name: experience-distiller
description: Turn a completed successful interaction into a privacy-reviewed candidate, then recommend and promote a reusable experience, workflow, script, skill, rule, or optional memory pointer in a user-specified private Git repository.
---
```

随后说明必须相对该 Skill 目录读取 `references/`、`templates/`、`scripts/`；禁止假定公开项目或私有库的绝对路径。

- [ ] **Step 2: 写入会话末尾执行协议**

按固定顺序要求 Agent：确认用户显式调用且提供私有库根；若缺少根则只询问路径；进行只读检索和去重；筛查敏感内容；生成候选草案和六类分类建议；展示目标相对路径、证据缺口和拟写内容；仅在用户批准后写 `candidates/`；仅在证据验证后升格；最后可选生成不超过一段的 Memory 指针建议。

- [ ] **Step 3: 写入安全失败模式**

要求在以下情况停止写入并报告原因：私有库根不明确、路径不在用户明确范围、内容含疑似凭据或真实个人数据、候选与已有卡冲突、验证证据不足却请求升格、或 Agent 不具备安全写入权限。禁止自动创建远程仓库、推送、安装其他工具或修改用户级 Agent 配置。

- [ ] **Step 4: 文本级一致性检查**

Run: `rg -n 'private repository|proposed_kind|memory_cache|approval|references/' skills/experience-distiller/SKILL.md`

Expected: 主指令明确覆盖私有目标、分类、可选缓存、审批和自身资源定位。

### Task 6: 编写五个最小适配器和项目文档链接

**Files:**

- Create: `adapters/codex.md`
- Create: `adapters/claude-code.md`
- Create: `adapters/cursor.md`
- Create: `adapters/copilot.md`
- Create: `adapters/generic-harness.md`
- Modify: `README.md`

- [ ] **Step 1: 为每个适配器采用同一四段格式**

固定二级标题为：`## Skill discovery`、`## Private repository input`、`## End-of-conversation invocation`、`## Optional memory cache`。每份文档必须说明：仅安装/映射公开 Skill；私有库位置由用户明确提供；调用发生在会话末尾；Memory 只能保存摘要与来源指针；不安装 MCP/插件、不复制事实库。

- [ ] **Step 2: 添加各环境的最小差异**

Codex 文档说明仓库/会话级 Skill 发现；Claude Code 说明项目指令或命令入口；Cursor 和 Copilot 说明规则/提示入口；通用 harness 说明直接读取 `SKILL.md` 并把私有库根作为显式参数。所有命令示例只使用 `<private-experience-repo>` 占位符，不能给出真实路径。

- [ ] **Step 3: 从 README 链接所有适配器和规范**

Run: `rg -n 'adapters/(codex|claude-code|cursor|copilot|generic-harness)\.md|experience-distiller' README.md`

Expected: README 含五个相对链接，并把公开 Skill 标为唯一安装对象。

### Task 7: 端到端公开性与跨平台验证

**Files:**

- Modify: `README.md`
- Modify: `tests/test_validate_library.py`

- [ ] **Step 1: 增加 UTF-8 和公开隐私启发式测试**

新增测试创建临时卡，分别包含 `C:\\Users\\example` 和 `api_key = example`；校验器须以明确的“possible public privacy issue”错误拒绝它们。该测试只使用虚构文本，不读取环境变量或真实配置。

- [ ] **Step 2: 执行完整测试**

Run: `python -m unittest discover -s tests -v`

Expected: 全部测试为 `ok`，无网络访问、无第三方安装、无用户级配置写入。

- [ ] **Step 3: 运行 Windows/WSL/macOS 可复制冒烟命令**

在 README 给出同一命令：

```text
python skills/experience-distiller/scripts/validate_library.py examples/sanitized
```

Windows PowerShell、WSL shell 和 macOS shell 均只需在项目根运行它；预期返回码为 `0`。

- [ ] **Step 4: 最终公开内容扫描**

Run: `rg -n -i 'C:\\Users\\ASUS|D:\\Desktop|/home/[^<]|(api[_-]?key|token|password)\s*[:=]\s*[^< ]+' -g '!spec/v1-design.md' -g '!spec/v1-implementation-plan.md' .`

Expected: 无匹配；若匹配，先脱敏或删除再继续，不得发布。

## 实施后人工检查

1. 确认 Skill 可作为 `skills/experience-distiller/` 单目录交付，且所有引用都是相对路径。
2. 审阅 README 与 adapters，确认没有暗示自动安装、自动写入 Memory 或共享私有经验。
3. 审阅示例、fixture 与 Git diff，确认所有内容均为虚构且可公开。
4. 再次确认未创建远程仓库、未 push、未发布、未修改用户级 Agent 配置。

## 授权边界

本计划依据当前批准可执行本地 Git 初始化和工作区内文件创建；**Git 提交、远程仓库创建、push、公开发布、实际安装 Skill、修改用户级配置或写入真实私有经验库**均需届时另行明确授权。

