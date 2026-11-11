# Textwerk: an extensible text tool with a microkernel

Starter repository for Assignment 2 of **SDA2 Software Architecture**, BFH.

Frischwerk wants a small text processing tool that can grow without changing
its core: new processing steps arrive as plug-ins. Your group specifies the
plug-in contract, lets a coding agent build the core and three plug-ins, and
then implements extension requests it did not know before. You measure how
much of the core and of the contract had to change.

- What to do: [`docs/assignment.md`](docs/assignment.md)
- What the tool must do: [`docs/cli.md`](docs/cli.md)
- Deadline, dates, assessment criteria and AI policy: Moodle

## Getting started

### Prerequisites

- Python 3.10 or newer (no further packages)
- git and a GitHub account
- make (optional; the Makefile shows the plain `python3` commands)

### 1. Create your group's private repository

This repository is a template. One group member creates the group's copy:

1. On GitHub, click **Use this template → Create a new repository**.
2. Choose your account as the owner and set the visibility to **Private**.
3. In the new repository, open **Settings → Collaborators** and invite the
   other group members and the lecturer (`shoehn`).

Then everyone clones the group's repository:

```bash
git clone git@github.com:<owner>/<your-repo>.git
cd <your-repo>
```

### 2. Run the tests once

```bash
make test
```

There is no core yet, so every test fails: **FAILED (failures=17)**. If you
see this, your setup works.

## The steps

1. Set up: private copy, tests (above).
2. Write the plug-in contract in `docs/contract.md`, commit, tag `contract-v1`.
3. Define your criteria in `docs/criteria.md`, commit, tag `criteria-v1`.
4. Version 1: generate the core and three plug-ins with a coding agent,
   provide the fixtures, verify, measure, tag `v1`.
5. Version 2: fetch the extension requests, implement them one after the
   other (tags `er1`, `er2`, `er3`), verify, measure, tag `v2`.
6. Assess and reflect in `docs/report.md`.
7. Tag `a2-submission`, push all tags, and hand in the repository URL on Moodle.

Details: [`docs/assignment.md`](docs/assignment.md#steps).

## Fetching the extension requests

The extension requests are added to this starter repository later (the date
is on Moodle). To copy them into your group's repository:

```bash
git remote add starter <URL of the starter repository, see Moodle>
git fetch starter
git checkout starter/main -- docs/extension-requests.md tests/er
git commit -m "Add extension requests"
```

## Commands

| Command | What it does |
|---|---|
| `make test` | acceptance tests, version 1 |
| `make test-v2` | acceptance tests and extension request tests, version 2 |
| `make conformance` | the core does not know the plug-ins |
| `make bench` | start-up and run times → `bench/results/` (add `LEVEL=v2` for version 2) |
| `make impact` | changes in core, contract and plug-ins between your tags |

To run a single test file: `python3 -m unittest tests/acceptance/test_run.py -v`.

If your tool is not started with `python3 -m core`, set `TEXTWERK_CMD`
(see [`docs/cli.md`](docs/cli.md#starting-the-tool)).

## Repository layout

```
├── README.md
├── AGENTS.md              context for coding agents
├── Makefile
├── docs/
│   ├── assignment.md      scenario, steps, deliverables
│   ├── cli.md             external behaviour of the tool (binding)
│   ├── contract.md        template: your plug-in contract, the spec for the agent
│   ├── criteria.md        template: your criteria
│   └── report.md          template: results, assessment, reflection
├── ai-log/                how you used AI, and what it got wrong
├── shared/sample.txt      sample text
├── core/                  your core
├── plugins/               your plug-ins
├── fixtures/              two plug-in directories with faulty plug-ins, for the tests
├── tests/                 acceptance tests and conformance check
└── bench/                 measurement scripts and results/
```

## Contact

Sebastian Höhn, Bern University of Applied Sciences (BFH).
