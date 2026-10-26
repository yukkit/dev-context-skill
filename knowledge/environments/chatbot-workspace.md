# 当前 Codex 容器工作区

ID：chatbot-workspace
范围：本次会话提供的容器文件系统。以下是本环境路径，不代表用户电脑或其他服务器的目录，也不代表业务服务所连接的运行环境。

## 项目位置

| 项目 | 代码目录 |
| --- | --- |
| [dev-context-skill](../projects/dev-context-skill.md) | `/chatbot/dev-context` |
| [ofnil-agentic-rag](../projects/ofnil-agentic-rag.md) | `/chatbot/ofnil-agentic-rag` |

来源：会话提供的工作目录、实际 `pwd` 输出及业务项目的 `AGENTS.md`；上下文库目录已创建并经本地 Git 检查。
确认日期：2026-10-26

## Codex 配置入口

- 当前 `CODEX_HOME`：`/root/.codex`。
- 全局指令入口：`/root/.codex/AGENTS.md`。其内容是权威约定，使用时读原文件。

来源：本次会话只读取了 `CODEX_HOME` 这一环境变量，并检查了全局指令文件；没有读取模型凭据或其他环境变量值。
确认日期：2026-10-26

## dev-context-skill 的 GitHub 访问

- 用户要求该仓库使用其本地 Git 凭据，不使用 makaili GitHub 连接器。
- 用户级 Git credential helper 的配置入口是 `/root/.gitconfig`。通过 `git credential fill` 获取凭据时设置 `GIT_CONFIG_NOSYSTEM=1`，避免混入系统级 helper 的账号。
- 该用户级凭据经 GitHub `/user` 接口确认为 `yukkit`，已成功用于设置仓库描述；凭据值只在操作进程内使用，不输出或写入记录。
- 当前仓库推送使用 SSH；GitHub API 元数据操作使用上述本地凭据。后续操作仍需遵守当次任务的授权范围。

来源：用户于 2026-10-26 明确指定凭据来源；实际通过用户级 Git helper 完成 GitHub 账号验证、仓库描述更新和回读校验。
确认日期：2026-10-26
