from pathlib import Path
import tempfile
import unittest

from scripts.install import END, START, install


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.repo = self.root / "repo with spaces"
        skill = self.repo / "skills/development-context/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("test skill", encoding="utf-8")
        index = self.repo / "knowledge/index.md"
        index.parent.mkdir()
        index.write_text("test index", encoding="utf-8")
        self.home = self.root / "home"
        self.codex = self.home / ".codex"
        self.codex.mkdir(parents=True)

    def test_installs_link_preserves_guidance_and_is_idempotent(self):
        target = self.codex / "AGENTS.md"
        target.write_text("原有约定\n", encoding="utf-8")
        target.chmod(0o640)
        link, guidance = install(self.repo, self.home, self.codex)
        first = guidance.read_bytes()
        self.assertTrue(first.decode().startswith("原有约定\n"))
        self.assertEqual(link.resolve(), self.repo / "skills/development-context")
        self.assertEqual(target.stat().st_mode & 0o777, 0o640)
        install(self.repo, self.home, self.codex)
        self.assertEqual(guidance.read_bytes(), first)

    def test_updates_active_override_and_preserves_symlink(self):
        ordinary = self.codex / "AGENTS.md"
        ordinary.write_text("base", encoding="utf-8")
        original = self.root / "shared-guidance.md"
        original.write_text("override", encoding="utf-8")
        override = self.codex / "AGENTS.override.md"
        override.symlink_to(original)
        _, guidance = install(self.repo, self.home, self.codex)
        self.assertEqual(guidance, original)
        self.assertTrue(override.is_symlink())
        self.assertIn(START, original.read_text())
        self.assertEqual(ordinary.read_text(), "base")

    def test_conflicting_skill_is_not_overwritten(self):
        link = self.home / ".agents/skills/development-context"
        link.mkdir(parents=True)
        with self.assertRaises(ValueError):
            install(self.repo, self.home, self.codex)
        self.assertFalse((self.codex / "AGENTS.md").exists())
        self.assertTrue(link.is_dir())

    def test_malformed_markers_do_not_modify_files(self):
        target = self.codex / "AGENTS.md"
        for text in [START, END + START, START + END + END]:
            with self.subTest(text=text):
                target.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    install(self.repo, self.home, self.codex)
                self.assertEqual(target.read_text(), text)
                self.assertFalse((self.home / ".agents/skills/development-context").exists())

    def test_reinstallation_updates_path_after_repository_move(self):
        link, guidance = install(self.repo, self.home, self.codex)
        old_path = str(self.repo)
        moved = self.root / "moved repo"
        self.repo.rename(moved)
        link.unlink()
        install(moved, self.home, self.codex)
        self.assertEqual(link.resolve(), moved / "skills/development-context")
        self.assertNotIn(old_path, guidance.read_text())
        self.assertEqual(guidance.read_text().count(START), 1)


if __name__ == "__main__":
    unittest.main()
