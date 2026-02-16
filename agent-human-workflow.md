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
