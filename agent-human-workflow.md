# Agent/Human Workflow Canary
#
# This file is append-only.
# Ignore blank lines and lines that start with "#".
#
# Line types:
# - AGENT ...  (written by agent when it starts file-writing work)
# - HUMAN ...  (written by human after review/vetting)
#
# AI-assisted PR gate rule:
# - For AI-assisted PRs, the latest meaningful line must match: HUMAN <text>
# - Minimum requirement for HUMAN lines: non-empty text after "HUMAN".
# - Recommended content for HUMAN lines: action/decision, date, git user/email.
#
# Example HUMAN line:
# HUMAN reviewed locally; ready for maintainer review; 2026-02-16; dev@example.com

HUMAN dre created the first entry on 2026-02-15 before testing an agent edit.
AGENT timestamp=2026-02-16T05:08:27Z; agent=codex; model=gpt-5; prompt="Create MovementGuide.md for core/search movement commands with links to docs and in-app references."
HUMAN dre this agent change wasn't caught by the validate-human-review-gate because the PR was created by me before the workflow existed. Will test it on my next PR though.
AGENT timestamp=2026-02-18T02:23:52Z; agent=codex; model=gpt-5; prompt="Revert the recent test-related ValueError-catching change for _get_colorpair()."
HUMAN dre change reviewed for push to PR
