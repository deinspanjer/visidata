#!/usr/bin/env python3
"""Validate AI-assisted PR human review canary requirements."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

AI_CHECKBOX_RE = re.compile(
    r"^\s*-\s*\[(?P<checked>[xX])\]\s*AI-assisted changes included\s*$",
    re.MULTILINE,
)
AI_TOKEN_RE = re.compile(r"^\s*AI_ASSISTED\s*:\s*true\s*$", re.IGNORECASE | re.MULTILINE)
HUMAN_LINE_RE = re.compile(r"^HUMAN\s+\S")

SAMPLE_HUMAN_LINE = "HUMAN reviewed locally; ready for maintainer review; 2026-02-16; dev@example.com"


def is_ai_assisted(pr_body: str) -> bool:
    return bool(AI_CHECKBOX_RE.search(pr_body) or AI_TOKEN_RE.search(pr_body))


def get_last_meaningful_line(canary_path: Path) -> str | None:
    if not canary_path.exists():
        return None

    last = None
    for raw_line in canary_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        last = line
    return last


def validate(pr_body: str, canary_path: Path) -> tuple[bool, str]:
    if not is_ai_assisted(pr_body):
        return True, "PR is not marked AI-assisted; human canary gate skipped."

    if not canary_path.exists():
        return (
            False,
            f"AI-assisted PR requires {canary_path} with a trailing HUMAN signoff line.\n"
            f"Add a line like:\n{SAMPLE_HUMAN_LINE}",
        )

    last_line = get_last_meaningful_line(canary_path)
    if last_line is None:
        return (
            False,
            f"AI-assisted PR requires a non-empty HUMAN signoff line in {canary_path}.\n"
            f"Add a line like:\n{SAMPLE_HUMAN_LINE}",
        )

    if not HUMAN_LINE_RE.match(last_line):
        return (
            False,
            "AI-assisted PR is blocked because the latest meaningful canary line is not "
            f"'HUMAN <text>': {last_line!r}\n"
            f"Append a line like:\n{SAMPLE_HUMAN_LINE}",
        )

    return True, "AI-assisted PR has valid trailing HUMAN signoff line."


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr-body", default="", help="Pull request body text")
    parser.add_argument("--head-sha", default="", help="PR head SHA (for context only)")
    parser.add_argument(
        "--canary",
        default="agent-human-workflow.md",
        help="Path to the append-only canary log",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    ok, message = validate(pr_body=args.pr_body or "", canary_path=Path(args.canary))

    if args.head_sha:
        print(f"Head SHA: {args.head_sha}")
    print(message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
