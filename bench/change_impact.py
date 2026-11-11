#!/usr/bin/env python3
"""What did the extension requests change? Compares git tags and counts files
and lines changed in the core, the contract, the plug-ins and the fixtures.

Usage: python3 bench/change_impact.py [from-tag to-tag]

Without arguments it reports v1 -> er1 -> er2 -> er3 if these tags exist (one
table per extension request), otherwise v1 -> v2. Prints Markdown; redirect it
into bench/results/ to keep it:

    python3 bench/change_impact.py > bench/results/impact.md
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles
AREAS = ["core", "docs/contract.md", "plugins", "fixtures"]


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def tag_exists(tag):
    return git("rev-parse", "-q", "--verify", f"refs/tags/{tag}").returncode == 0


def numstat(old, new, path):
    rows = []
    for line in git("diff", "--numstat", old, new, "--", path).stdout.splitlines():
        added, deleted, name = line.split("\t", 2)
        rows.append((name, 0 if added == "-" else int(added), 0 if deleted == "-" else int(deleted)))
    return rows


def status(old, new, path):
    """Added (A), modified (M), deleted (D), renamed (R) files."""
    counts = {}
    for line in git("diff", "--name-status", old, new, "--", path).stdout.splitlines():
        counts[line[0]] = counts.get(line[0], 0) + 1
    return counts


def report(old, new):
    print(f"## {old} → {new}\n")
    print("| Area | Files changed | New files | Lines added | Lines deleted |")
    print("|---|---|---|---|---|")
    for area in AREAS:
        rows = numstat(old, new, area)
        new_files = status(old, new, area).get("A", 0)
        print(f"| `{area}` | {len(rows)} | {new_files} | "
              f"{sum(r[1] for r in rows)} | {sum(r[2] for r in rows)} |")
    core = numstat(old, new, "core")
    if core:
        print("\nCore files touched:\n")
        for name, added, deleted in core:
            print(f"- `{name}`: +{added} −{deleted}")
    else:
        print("\nThe core was not changed.")
    existing = [line.split("\t")[-1] for line in
                git("diff", "--name-status", "--diff-filter=MDR", old, new, "--", "plugins").stdout.splitlines()]
    if existing:
        print("\nExisting plug-in files changed or removed:\n")
        for name in existing:
            print(f"- `{name}`")
    print()


if len(sys.argv) == 3:
    steps = [(sys.argv[1], sys.argv[2])]
elif all(tag_exists(tag) for tag in ("v1", "er1", "er2", "er3")):
    steps = [("v1", "er1"), ("er1", "er2"), ("er2", "er3")]
else:
    steps = [("v1", "v2")]

for old, new in steps:
    missing = [tag for tag in (old, new) if not tag_exists(tag)]
    if missing:
        sys.exit(f"tag not found: {', '.join(missing)}")
    report(old, new)
if len(steps) == 3:
    report("v1", "er3")
