import os
from pathlib import Path
import stat
import tempfile


START = "<!-- development-context:start -->"
END = "<!-- development-context:end -->"


def merged_guidance(existing, skill_path):
    block = f"""{START}
## 开发上下文

涉及项目、环境、配置或操作流程的任务，先读取 `{skill_path}`，按其中流程查找相关上下文；用户提供或纠正可复用事实时，按该技能更新本地记录。只读取当前任务所需条目，记录不扩大执行权限。
{END}"""
    if START not in existing and END not in existing:
        return existing + ("\n\n" if existing else "") + block + "\n"
    if existing.count(START) != 1 or existing.count(END) != 1:
        raise ValueError("全局指令中的 development-context 标记不完整或重复；请先检查该文件")
    before, _, remainder = existing.partition(START)
    _, separator, after = remainder.partition(END)
    if not separator:
        raise ValueError("全局指令中的 development-context 标记顺序错误")
    return before + block + after


def install(repo_root, user_home, codex_home):
    skill = (repo_root / "skills/development-context").resolve()
    if not (skill / "SKILL.md").is_file() or not (repo_root / "knowledge/index.md").is_file():
        raise ValueError("请从完整的 dev-context 仓库运行安装脚本")
    link = user_home / ".agents/skills/development-context"
    if (link.exists() or link.is_symlink()) and not (link.is_symlink() and link.resolve() == skill):
        raise ValueError(f"已有其他技能占用 {link}；未覆盖")

    override = codex_home / "AGENTS.override.md"
    guidance = override if override.is_file() and override.read_text(encoding="utf-8").strip() else codex_home / "AGENTS.md"
    guidance = guidance.resolve()
    existing = guidance.read_text(encoding="utf-8") if guidance.exists() else ""
    updated = merged_guidance(existing, skill / "SKILL.md")

    link.parent.mkdir(parents=True, exist_ok=True)
    if not link.is_symlink():
        link.symlink_to(skill, target_is_directory=True)
    if updated != existing:
        guidance.parent.mkdir(parents=True, exist_ok=True)
        mode = stat.S_IMODE(guidance.stat().st_mode) if guidance.exists() else 0o600
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=guidance.parent, delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(updated)
            temporary.chmod(mode)
            temporary.replace(guidance)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
    return link, guidance


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    user_home = Path.home()
    codex_home = Path(os.environ.get("CODEX_HOME") or user_home / ".codex").expanduser()
    try:
        link, guidance = install(repo_root, user_home, codex_home)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error))
    print(f"技能入口：{link}")
    print(f"全局指令：{guidance}")
    print("已保留原有指令。请在新的 Codex 会话中检查技能和全局入口是否可见。")
