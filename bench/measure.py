#!/usr/bin/env python3
"""Start-up and run times of the tool, with and without plug-ins.

Usage: python3 bench/measure.py [level]        (level: v1 or v2, default v1)
Writes bench/results/times-<level>.csv and prints a summary.

Each measurement starts the tool as a new process, so the numbers include the
start of the interpreter and the discovery of the plug-ins. This is a starting
point: add what your own criteria need.
"""
import csv
import pathlib
import statistics
import sys
import tempfile
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tests"))
import textwerk as tw

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles
RUNS = 15
level = sys.argv[1] if len(sys.argv) > 1 else "v1"


def timed(*args, plugins_dir=None):
    samples = []
    for _ in range(RUNS):
        start = time.perf_counter()
        result = tw.run(*args, plugins_dir=plugins_dir)
        samples.append((time.perf_counter() - start) * 1000)
        if result.returncode != 0:
            sys.exit(f"command failed: {' '.join(map(str, args))}\n{result.stderr}")
    return statistics.median(samples), min(samples), max(samples)


def chain(names):
    return [item for name in names for item in ("--plugin", name)]


with tempfile.TemporaryDirectory() as tmp:
    tmp = pathlib.Path(tmp)
    empty = tmp / "empty"
    empty.mkdir()
    out = tmp / "out.txt"
    base = ["run", "--input", tw.SAMPLE, "--output", out]
    names = tw.plugin_names()
    if not names:
        sys.exit("no plug-ins listed: `python3 -m core list` must work first")

    rows = [
        ("list, no plug-ins", *timed("list", plugins_dir=empty)),
        (f"list, {len(names)} plug-ins", *timed("list")),
        ("run, no plug-ins available", *timed(*base, plugins_dir=empty)),
        ("run, plug-ins available, none applied", *timed(*base)),
    ]
    for name in names:
        result = tw.run(*base, "--plugin", name)
        if result.returncode != 0:
            print(f"skipped {name}: needs parameters or failed (exit {result.returncode})")
            continue
        rows.append((f"run, 1 plug-in ({name})", *timed(*base, "--plugin", name)))

results = tw.ROOT / "bench" / "results"
results.mkdir(parents=True, exist_ok=True)
target = results / f"times-{level}.csv"
with target.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["case", "median_ms", "min_ms", "max_ms", "runs"])
    for case, median, low, high in rows:
        writer.writerow([case, f"{median:.1f}", f"{low:.1f}", f"{high:.1f}", RUNS])

print(f"| Case | Median (ms) | Min | Max |\n|---|---|---|---|")
for case, median, low, high in rows:
    print(f"| {case} | {median:.1f} | {low:.1f} | {high:.1f} |")
print(f"\nWritten to {target.relative_to(tw.ROOT)}")
