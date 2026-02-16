# VisiData Development Guide

Quick reference for VisiData development. For detailed coding patterns, conventions, and best practices, see **[dev/STYLE.md](dev/STYLE.md)**.

## Important Note About AI Usage

VisiData (created in 2016) is 99% written by humans and is NOT a vibe-coded AI project.  This file is meant to allow AI-assisted development of features and bugfixes.  **All code must be reviewed and approved and tested by a human before being merged into the codebase or submitted as a PR.**

## Human Review Canary Workflow (AI-Assisted Code Rules)
- Use `agent-human-workflow.md` as an append-only canary log.
- Pre-edit gate (mandatory):
  - Before the first write to any repository file in a turn (code, docs, tests, configs), the agent must check the latest meaningful canary line.
  - If the latest meaningful line is `HUMAN ...`, append exactly one `AGENT ...` line immediately before making any other repo edit.
  - If the latest meaningful line is `AGENT ...`, do not append another `AGENT` line for that turn.
  - Hard fail: if this check/update is not completed, do not edit any repository files.
- Mechanical check command (required before first edit in a turn):
  - `tail agent-human-workflow.md`
- Pre-push gate (mandatory):
  - Before pushing a branch to a GitHub remote, the agent must attempt to check if the branch is associated with a PR.
  - If the `gh` command is available and authenticated, execute `gh pr view --json number,url,state --jq '.'`
  - If the command returns PR data, agent must follow this workflow's Agent behavior rule.
  - Else, push is allowed.
- `AGENT` line format (minimum required fields):
  - `AGENT timestamp=<UTC ISO8601>; agent=<name>; model=<model>; prompt="<first-prompt-summary>"`
- Agent behavior:
  - Agent may commit to a branch.
  - On the first repo write in a turn, follow the pre-edit gate above.
  - Agent must not create or submit an AI-assisted PR unless the latest meaningful canary line matches `HUMAN <text>`.
  - Agent must not push changes to a PR-linked branch unless the latest meaningful canary line matches `HUMAN <text>`.
  - If blocked, ask the human to append a `HUMAN` line describing what they did to review/vet the changes.
- Human signoff line requirements:
  - Minimum: line begins with `HUMAN` and includes non-empty text after the prefix.
  - Recommended (not required): action/decision, date, and git user/email.

## Repository Structure

```
visidata/
├── visidata/              # Main package
│   ├── *.py              # Core modules (sheet.py, column.py, etc.)
│   ├── features/         # Auto-loaded feature plugins
│   ├── loaders/          # File format loaders
│   ├── apps/             # Standalone applications
│   └── experimental/     # Experimental features (load/install with 'import visidata.experimental.foo')
├── tests/                # Test files
├── docs/                 # Documentation
└── dev/                  # Development utilities and docs
```

## Features Directory (`visidata/features/`)

- All `.py` files in this directory are **automatically imported** when VisiData starts
- Each feature file should be self-contained
- Features extend VisiData functionality without modifying core files

## Quick Reference

### Core Classes
- `BaseSheet` - Minimal sheet functionality
- `Sheet` / `TableSheet` - Sheet with columns and rows (most common)
- `Column` - Column definition with getter/setter

### Adding Commands
```python
BaseSheet.addCommand('', 'command-name', 'code', 'help text')
```

### Adding to Global Namespace
```python
vd.addGlobals(MyClass=MyClass)  # Use keyword args, not dict
```

### Adding Menu Items
```python
vd.addMenuItems('''
    Menu > Submenu > Item Name > command-name
''')
```

### Example Feature Structure
```python
from visidata import vd, Sheet, Column

# rowdef: description of what a row represents
class MySheet(Sheet):
    rowtype = 'items'
    columns = [
        Column('name', getter=lambda c,r: r.attribute),
    ]

    def reload(self):
        self.rows = [...]

BaseSheet.addCommand('', 'my-command', 'code', 'help')
vd.addGlobals(MySheet=MySheet)
```

## Development Workflow

1. Add `.py` file to `visidata/features/`
2. Run `vd` and test interactively
3. Iterate and refine
4. Document with docstrings and comments

## Documentation

For comprehensive development documentation, see the `dev/` directory:

### [dev/STYLE.md](dev/STYLE.md) - Coding Style and Patterns
Use this when writing code, creating features, or defining sheets and columns.
- Naming conventions (camelCaps, under_score, etc.)
- Feature file structure and patterns
- Sheet and Column class patterns
- Command and menu integration
- API decorators
- Best practices and examples

### [dev/GIT.md](dev/GIT.md) - Version Control Practices
Use this when making commits or preparing pull requests.
- Commit message format and conventions
- Issue tracking in code
- Branch and merge workflow
- Patch-safe commit marking

### [dev/DOCS.md](dev/DOCS.md) - Documentation Writing
Use this when writing user-facing documentation, help text, or in-app guides.
- VisiData's markdown syntax
- Display attribute syntax (colors, clickable links)
- Option and command reference format
- Technical writing guidelines

### [dev/PERFORMANCE.md](dev/PERFORMANCE.md) - Performance Analysis
Use this when investigating or optimizing performance issues.
- Finding reproducible performance issues
- Profiling techniques and tools
- Analyzing profiling results
- Optimization workflow
