import importlib.util
from importlib.machinery import SourceFileLoader
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "bin" / "init-agent-memory"
DREAMING_SKILL = ROOT / "templates" / "skills" / "dreaming" / "SKILL.md"
SPEC = importlib.util.spec_from_loader(
    "init_agent_memory", SourceFileLoader("init_agent_memory", str(SCRIPT))
)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class InitAgentMemoryTests(unittest.TestCase):
    def make_repo(self, name="repo"):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        repo = Path(temporary.name) / name
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        return repo

    def run_cli(self, repo, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args, str(repo)],
            capture_output=True,
            text=True,
        )

    def test_new_repository_and_idempotence(self):
        repo = self.make_repo()
        first = self.run_cli(repo)
        self.assertEqual(first.returncode, 0, first.stderr)
        if os.name == "nt":
            self.assertEqual((repo / "CLAUDE.md").read_text(), "@AGENTS.md\n")
        else:
            self.assertTrue((repo / "CLAUDE.md").is_symlink())
            self.assertEqual((repo / "CLAUDE.md").readlink(), Path("AGENTS.md"))
        self.assertIn("only durable project-memory store", (repo / "AGENTS.md").read_text())
        self.assertIn(
            "Where durable knowledge belongs",
            (repo / "AgentMemories" / "README.md").read_text(),
        )
        self.assertIn(
            MODULE.MEMORY_START_MARKER,
            (repo / "AgentMemories" / "README.md").read_text(),
        )
        self.assertIn(
            "follow the knowledge-placement order",
            (repo / "AGENTS.md").read_text(),
        )
        installed_skill = repo / ".agents" / "skills" / "dreaming" / "SKILL.md"
        self.assertEqual(installed_skill.read_text(), DREAMING_SKILL.read_text())
        if os.name == "nt":
            self.assertFalse((repo / ".claude" / "skills").exists())
        else:
            self.assertEqual(
                (repo / ".claude" / "skills").readlink(),
                Path("../.agents/skills"),
            )
        self.assertEqual(
            json.loads((repo / ".claude" / "settings.json").read_text()),
            {"autoMemoryEnabled": False},
        )
        second = self.run_cli(repo)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("no changes needed", second.stdout)

    def test_path_with_spaces(self):
        repo = self.make_repo("repo with spaces")
        result = self.run_cli(repo)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_dreaming_skill_can_be_explicitly_skipped(self):
        repo = self.make_repo()
        result = self.run_cli(repo, "--no-dreaming")
        self.assertEqual(result.returncode, 0, result.stderr)
        config = repo / ".agents" / "agnostic-agent-memory.json"
        self.assertEqual(json.loads(config.read_text()), {"dreaming": False})
        self.assertFalse((repo / ".agents" / "skills").exists())
        self.assertFalse((repo / ".claude" / "skills").exists())

        second = self.run_cli(repo)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("no changes needed", second.stdout)

        enabled = self.run_cli(repo, "--dreaming")
        self.assertEqual(enabled.returncode, 0, enabled.stderr)
        self.assertEqual(json.loads(config.read_text()), {"dreaming": True})
        self.assertEqual(
            (repo / ".agents" / "skills" / "dreaming" / "SKILL.md").read_text(),
            DREAMING_SKILL.read_text(),
        )

    def test_opt_out_preserves_an_existing_dreaming_skill(self):
        repo = self.make_repo()
        skill = repo / ".agents" / "skills" / "dreaming" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("custom dreaming workflow\n")

        result = self.run_cli(repo, "--no-dreaming")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(skill.read_text(), "custom dreaming workflow\n")

    def test_existing_dreaming_skill_requires_confirmation(self):
        repo = self.make_repo()
        skill = repo / ".agents" / "skills" / "dreaming" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("custom dreaming workflow\n")

        result = self.run_cli(repo)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(skill.read_text(), "custom dreaming workflow\n")
        self.assertFalse((repo / "AGENTS.md").exists())

        approved = self.run_cli(repo, "--yes")
        self.assertEqual(approved.returncode, 0, approved.stderr)
        self.assertEqual(skill.read_text(), DREAMING_SKILL.read_text())

    def test_copied_initializer_requires_its_canonical_sources(self):
        repo = self.make_repo()
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        standalone = Path(temporary.name) / "init-agent-memory"
        shutil.copy2(SCRIPT, standalone)
        result = subprocess.run(
            [sys.executable, str(standalone), str(repo)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("must run from an agnostic-agent-memory checkout", result.stderr)
        self.assertFalse((repo / "AGENTS.md").exists())

    @unittest.skipIf(os.name == "nt", "symlink creation needs elevated Windows privileges")
    def test_initializer_runs_through_a_symlink(self):
        repo = self.make_repo()
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        command = Path(temporary.name) / "init-agent-memory"
        command.symlink_to(SCRIPT)
        result = subprocess.run(
            [sys.executable, str(command), str(repo)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((repo / "AGENTS.md").is_file())

    def test_existing_agents_requires_confirmation(self):
        repo = self.make_repo()
        original = "# Existing instructions\n\nKeep this.\n"
        (repo / "AGENTS.md").write_text(original)
        result = self.run_cli(repo)
        self.assertEqual(result.returncode, 2)
        self.assertEqual((repo / "AGENTS.md").read_text(), original)
        self.assertFalse((repo / "AgentMemories").exists())

    def test_yes_appends_without_replacing_existing_agents(self):
        repo = self.make_repo()
        (repo / "AGENTS.md").write_text("# Existing instructions\n\nKeep this.\n")
        result = self.run_cli(repo, "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        content = (repo / "AGENTS.md").read_text()
        self.assertTrue(content.startswith("# Existing instructions\n\nKeep this.\n"))
        self.assertEqual(content.count(MODULE.START_MARKER), 1)

    def test_existing_memory_index_requires_confirmation(self):
        repo = self.make_repo()
        memory = repo / "AgentMemories" / "README.md"
        memory.parent.mkdir()
        memory.write_text("# Existing memory index\n\n- Keep this.\n")
        result = self.run_cli(repo)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(memory.read_text(), "# Existing memory index\n\n- Keep this.\n")
        self.assertFalse((repo / "AGENTS.md").exists())

    def test_yes_appends_policy_without_replacing_existing_memory_index(self):
        repo = self.make_repo()
        memory = repo / "AgentMemories" / "README.md"
        memory.parent.mkdir()
        memory.write_text("# Existing memory index\n\n- Keep this.\n")
        result = self.run_cli(repo, "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        content = memory.read_text()
        self.assertTrue(content.startswith("# Existing memory index\n\n- Keep this.\n"))
        self.assertEqual(content.count(MODULE.MEMORY_START_MARKER), 1)

    def test_update_preserves_memory_index_entries(self):
        repo = self.make_repo()
        first = self.run_cli(repo)
        self.assertEqual(first.returncode, 0, first.stderr)
        memory = repo / "AgentMemories" / "README.md"
        content = memory.read_text().replace(
            "Skills are procedures", "Skills were procedures"
        )
        memory.write_text(content + "\n## Index\n\n- [Decision](decision.md)\n")
        result = self.run_cli(repo, "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        updated = memory.read_text()
        self.assertIn("Skills are procedures", updated)
        self.assertNotIn("Skills were procedures", updated)
        self.assertIn("- [Decision](decision.md)", updated)

    def test_conflicting_claude_file_is_preserved_without_confirmation(self):
        repo = self.make_repo()
        (repo / "CLAUDE.md").write_text("Existing Claude instructions\n")
        result = self.run_cli(repo)
        self.assertEqual(result.returncode, 2)
        self.assertEqual((repo / "CLAUDE.md").read_text(), "Existing Claude instructions\n")
        self.assertFalse((repo / "AGENTS.md").exists())

    def test_include_mode_replaces_conflict_with_confirmation(self):
        repo = self.make_repo()
        (repo / "CLAUDE.md").write_text("Existing\n")
        result = self.run_cli(repo, "--yes", "--claude-mode", "include")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((repo / "CLAUDE.md").is_symlink())
        self.assertEqual((repo / "CLAUDE.md").read_text(), "@AGENTS.md\n")
        self.assertTrue(
            (repo / ".agents" / "skills" / "dreaming" / "SKILL.md").is_file()
        )
        self.assertFalse((repo / ".claude" / "skills").exists())

    @unittest.skipIf(os.name == "nt", "symlink creation needs elevated Windows privileges")
    def test_existing_project_skills_are_linked_for_claude(self):
        repo = self.make_repo()
        skill = repo / ".agents" / "skills" / "example" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("---\nname: example\ndescription: Example skill.\n---\n")
        result = self.run_cli(repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((repo / ".claude" / "skills").readlink(), Path("../.agents/skills"))

    def test_existing_claude_settings_are_merged(self):
        repo = self.make_repo()
        settings = repo / ".claude" / "settings.json"
        settings.parent.mkdir()
        settings.write_text('{"permissions": {"allow": ["Read"]}}\n')
        result = self.run_cli(repo, "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        updated = json.loads(settings.read_text())
        self.assertEqual(updated["permissions"], {"allow": ["Read"]})
        self.assertIs(updated["autoMemoryEnabled"], False)

    def test_invalid_claude_settings_abort_before_writes(self):
        repo = self.make_repo()
        settings = repo / ".claude" / "settings.json"
        settings.parent.mkdir()
        settings.write_text("not json\n")
        result = self.run_cli(repo, "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((repo / "AGENTS.md").exists())

    def test_invalid_agent_memory_config_aborts_before_writes(self):
        repo = self.make_repo()
        config = repo / ".agents" / "agnostic-agent-memory.json"
        config.parent.mkdir()
        config.write_text("not json\n")
        result = self.run_cli(repo)
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot safely read invalid JSON", result.stderr)
        self.assertFalse((repo / "AGENTS.md").exists())

    def test_dry_run_does_not_write(self):
        repo = self.make_repo()
        result = self.run_cli(repo, "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dry run", result.stdout)
        self.assertFalse((repo / "AGENTS.md").exists())

    @unittest.skipIf(os.name == "nt", "symlink creation needs elevated Windows privileges")
    def test_external_memory_directory_symlink_is_rejected(self):
        repo = self.make_repo()
        external = repo.parent / "external-memory"
        external.mkdir()
        (repo / "AgentMemories").symlink_to(external, target_is_directory=True)
        result = self.run_cli(repo, "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("must not be a symlink", result.stderr)
        self.assertFalse((external / "README.md").exists())

    @unittest.skipIf(os.name == "nt", "symlink creation needs elevated Windows privileges")
    def test_external_skills_directory_symlink_is_rejected(self):
        repo = self.make_repo()
        external = repo.parent / "external-skills"
        external.mkdir()
        (repo / ".agents").symlink_to(external, target_is_directory=True)
        result = self.run_cli(repo, "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("project skills directory must not be a symlink", result.stderr)
        self.assertFalse((external / "skills" / "README.md").exists())

    @unittest.skipIf(os.name == "nt", "symlink creation needs elevated Windows privileges")
    def test_symlinked_agents_file_is_rejected(self):
        repo = self.make_repo()
        external = repo.parent / "external-agents.md"
        external.write_text("# External\n")
        (repo / "AGENTS.md").symlink_to(external)
        result = self.run_cli(repo, "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("refusing to modify symlinked instructions", result.stderr)
        self.assertEqual(external.read_text(), "# External\n")

    @unittest.skipIf(os.name == "nt", "symlink creation needs elevated Windows privileges")
    def test_dangling_agents_symlink_is_rejected(self):
        repo = self.make_repo()
        (repo / "AGENTS.md").symlink_to(repo.parent / "missing-agents.md")
        result = self.run_cli(repo, "--yes")
        self.assertEqual(result.returncode, 2)
        self.assertIn("refusing to modify symlinked instructions", result.stderr)


if __name__ == "__main__":
    unittest.main()
