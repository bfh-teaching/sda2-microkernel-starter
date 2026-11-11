# AGENTS.md

Context for coding agents working in this repository.

## What this repository is

A teaching project. A group builds a small text processing tool with a
microkernel architecture: a core and plug-ins. Later it implements extension
requests and measures how much of the core had to change. You implement the
core and the plug-ins from the group's plug-in contract.

## Sources of truth, in this order

1. [`docs/cli.md`](docs/cli.md): the external behaviour of the tool. For
   version 2 also `docs/extension-requests.md`. **Binding.**
2. [`docs/contract.md`](docs/contract.md): the group's plug-in contract.
   Follow it. If it contradicts 1, or leaves a decision open, stop and ask.
   If you cannot ask, decide, and add the decision to `docs/contract.md`
   under "Decisions taken by the agent" so that the group can review it.

## Layout

```
docs/       cli.md (binding), contract.md (the spec), criteria.md, report.md, assignment.md
core/       the core: finds, loads and runs plug-ins; reads and writes files
plugins/    the plug-ins, one unit per plug-in, in the form the contract defines
fixtures/   two plug-in directories with faulty plug-ins for the tests
shared/     sample text (read-only)
tests/      acceptance tests and conformance check (read-only)
bench/      measurement scripts and results/
ai-log/     the group's log of AI use
```

## Do not change

- `tests/`
- `shared/`
- `docs/cli.md`, `docs/extension-requests.md`

If a test seems wrong, report it to the group; do not change it, and do not
write code that detects the test environment.

## Rules for the core

- The core does not know any plug-in by name and does not import a plug-in
  statically. It finds plug-ins at run time in `plugins/`, or in the
  directory named by the environment variable `TEXTWERK_PLUGINS`.
- The tool runs without any plug-in.
- A plug-in that cannot be loaded, or that fails while processing, does not
  crash the core (see "Errors" in `docs/cli.md`).
- When a new requirement arrives, solve it with a plug-in if the contract
  allows it. Do not change the core or the contract without telling the
  group; if a change is needed, say why a plug-in alone is not enough.

## Conventions

- Python 3.10 or newer is recommended, standard library only. Another
  language is allowed if the tool offers the same command-line interface;
  then the group sets `TEXTWERK_CMD`.
- The default start command is `python3 -m core` from the repository root.
- Text files are UTF-8.

## Commands

| Command | What it does |
|---------|--------------|
| `make test` | acceptance tests, version 1 |
| `make test-v2` | acceptance tests and extension request tests, version 2 |
| `make conformance` | the core does not know the plug-ins |
| `make bench` | start-up and run times, written to `bench/results/` |
| `make impact` | changes in core, contract and plug-ins between the tags |

Without make: see the Makefile for the underlying `python3` commands.

## Definition of done

- Version 1: `make test` and `make conformance` pass.
- Version 2: `make test-v2` and `make conformance` pass.
- The code does what `docs/contract.md` says. Where you deviated, say so.
- Nothing in the "Do not change" list was changed.
