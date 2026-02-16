import subprocess
import sys
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "dev"
    / "checks"
    / "validate_human_review_gate.py"
)


def run_gate(tmp_path, pr_body, canary_text=None):
    canary_path = tmp_path / "agent-human-workflow.md"
    if canary_text is not None:
        canary_path.write_text(canary_text, encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--pr-body",
            pr_body,
            "--head-sha",
            "deadbeef",
            "--canary",
            str(canary_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def test_non_ai_pr_passes_without_canary(tmp_path):
    code, output = run_gate(tmp_path, pr_body="- [ ] AI-assisted changes included", canary_text=None)
    assert code == 0
    assert "gate skipped" in output


def test_ai_pr_fails_when_canary_missing(tmp_path):
    code, output = run_gate(tmp_path, pr_body="- [x] AI-assisted changes included", canary_text=None)
    assert code == 1
    assert "requires" in output


def test_ai_pr_fails_when_latest_line_is_agent(tmp_path):
    code, output = run_gate(
        tmp_path,
        pr_body="- [x] AI-assisted changes included",
        canary_text="HUMAN reviewed earlier\nAGENT 2026-02-16 12:01 codex gpt-5 first-prompt=foo\n",
    )
    assert code == 1
    assert "not 'HUMAN <text>'" in output


def test_ai_pr_fails_when_human_line_has_no_text(tmp_path):
    code, output = run_gate(
        tmp_path,
        pr_body="- [x] AI-assisted changes included",
        canary_text="HUMAN\n",
    )
    assert code == 1
    assert "not 'HUMAN <text>'" in output


def test_ai_pr_passes_with_valid_human_line(tmp_path):
    code, output = run_gate(
        tmp_path,
        pr_body="- [x] AI-assisted changes included",
        canary_text="HUMAN reviewed and tested\n",
    )
    assert code == 0
    assert "valid trailing HUMAN" in output


def test_ai_pr_ignores_trailing_blank_and_comment_lines(tmp_path):
    code, output = run_gate(
        tmp_path,
        pr_body="- [x] AI-assisted changes included",
        canary_text="HUMAN reviewed and tested\n\n# trailing comment\n",
    )
    assert code == 0
    assert "valid trailing HUMAN" in output


def test_ai_pr_fails_on_lowercase_human_prefix(tmp_path):
    code, output = run_gate(
        tmp_path,
        pr_body="- [x] AI-assisted changes included",
        canary_text="human reviewed and tested\n",
    )
    assert code == 1
    assert "not 'HUMAN <text>'" in output
