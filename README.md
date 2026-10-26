# dev-context-skill

让 Codex 记住跨项目的开发上下文，按需读取并维护项目、环境、服务配置和操作流程。

当工作涉及多个仓库、开发机和服务时，代码在哪、配置在哪、项目简称指什么、某个环境如何启动，往往需要反复介绍。这个 Skill 将已确认的信息保存在本地 Markdown 中，让后续任务先查已有记录，并在信息变化时维护原条目。

## 工作方式

1. **全局入口提醒查询**：涉及项目、环境或操作流程时，Codex 先读取 `development-context` Skill。
2. **索引按需取资料**：按项目名、别名和环境找到相关条目，不把整个知识库加载进每次任务。
3. **核实后操作**：对本次任务依赖的路径、配置入口和命令做必要检查，区分机器和运行环境。
4. **随任务维护记录**：用户提供或纠正的长期信息、任务中核实的可复用事实，更新到对应条目，并保留来源和确认日期。

项目本身已有的 `AGENTS.md`、README、OpenSpec 和操作文档仍是维护入口。上下文库保存它们的位置与用途，避免维护两份规则。

## 快速安装

需要 Python 3、Git，以及能够读取本地技能和全局指令的 Codex 环境。安装器只使用 Python 标准库。

```sh
git clone https://github.com/yukkit/dev-context-skill.git
cd dev-context-skill
python3 scripts/install.py
```

已有本地仓库时，直接在仓库根目录运行最后一条命令。

安装会做两件事：

- 将 `~/.agents/skills/development-context` 软链接到本仓库的技能目录。
- 在 Codex 主目录（`CODEX_HOME`，默认 `~/.codex`）的全局指令中加入简短入口。存在生效的 `AGENTS.override.md` 时更新该文件，否则更新 `AGENTS.md`。

安装器保留原有指令，重复安装不会重复追加，也不覆盖同名的其他技能。安装和测试不会启动额外模型、业务服务或后台采集进程。

安装后新建 Codex 会话，检查是否能找到 `development-context`。Skill 的隐式匹配不能保证每次触发，全局入口也依赖客户端加载该文件；可显式使用 `$development-context` 调用。

## 使用示例

首次介绍一个项目：

> 记住：以后说“后台”就是项目 A，开发机上的目录是 /work/project-a，配置文件在该目录的 .env.dev。不要读取里面的密钥值。

更新某个环境：

> 项目 A 在笔记本上移到了 /Users/me/code/project-a，服务器上的目录不变，更新一下记录。

复用已有上下文：

> 先查开发上下文，再帮我启动后台。

查询目前记住的内容：

> 你现在记得哪些项目和环境？

除显式的“记住”请求外，Codex 在正常任务中也可保存已核实、值得复用的信息，并在完成回复中简短说明。没有相关变化时不产生新记录。

## 资料组织

| 位置 | 内容 |
| --- | --- |
| [Skill](skills/development-context/SKILL.md) | 查询、核实、更新记录的流程和权限边界 |
| [记录格式](skills/development-context/references/record-format.md) | 事实归属、来源、日期和命令验证状态的约定 |
| [知识索引](knowledge/index.md) | 项目、别名和环境的路由 |
| `knowledge/projects/` | 项目身份、仓库标识及权威文档入口 |
| `knowledge/environments/` | 各机器/环境中的代码路径、配置位置和运行方式 |
| `knowledge/services/` | 有实际需要时增加的跨项目服务资料 |
| `knowledge/runbooks/` | 有实际需要时增加的已验证操作流程 |

当前记录包含作者已确认的本库、ofnil-agentic-rag 入口及容器环境。其他使用者应替换为自己的信息；相同路径不能作为判断“这是同一台机器”的依据。不会通过扫描其他项目、历史会话或凭据文件自动充实资料。

## 记录边界

- 保存项目与别名的对应、环境映射、配置位置、服务依赖和可复用流程；不保存聊天流水账、完整日志、猜测或临时进程状态。
- 密码、token、私钥、cookie 和带认证参数的链接不进入记录，只保存配置路径、变量名或密钥管理器中的引用。
- 记录“如何部署、连接服务或调用模型”不构成执行授权，实际操作仍遵守当前任务的授权范围。
- 记录更新默认留在本地工作区。仅在用户要求时提交或推送，不自动同步到外部服务。

本仓库为公开仓库。个人知识也可能包含内部地址和项目名称，加入这类资料前应考虑使用自己的私有副本。`.gitignore` 不会检查文件内容，也无法清除已提交的敏感内容。

## 版本管理与换机器

需要保存版本时，可以让 Codex 提交，或在检查差异后手动提交：

```sh
git status --short
git diff
git add knowledge/
git diff --cached
git commit -m "Update development context"
```

推送到何处由使用者决定。多台机器使用时，先通过自己配置的远程同步记录，再在每台机器运行安装器，并分别维护环境映射。没有可访问的本地库或明确配置的同步时，其他机器和云端会话无法自动共享记录。

同一机器移动仓库时，先删除指向旧位置的 `~/.agents/skills/development-context` 软链接，再从新位置重新安装；全局指令中的路径也会更新。

## 卸载

删除安装器创建的 `~/.agents/skills/development-context` 软链接，再从安装输出指向的全局指令文件中删除 `<!-- development-context:start -->` 到 `<!-- development-context:end -->` 这一段，保留其他内容。知识文件仍留在仓库中。

## 开发与验证

在仓库根目录运行：

```sh
python3 -m unittest discover -s tests -v
```

测试使用临时目录，覆盖保留原指令、重复安装、生效的 override、冲突保护和移动仓库后的重新接入。Skill 可用 Codex 内置 `skill-creator` 提供的 `quick_validate.py` 校验，该校验器需要 PyYAML。上述验证不调用配置中的模型或外部服务。

设计依据：[OpenAI Skill 文档](https://learn.chatgpt.com/docs/build-skills)介绍技能按需加载和用户目录中的软链接；[全局 AGENTS.md 文档](https://learn.chatgpt.com/docs/agent-configuration/agents-md)介绍全局入口与 override 的加载顺序。
