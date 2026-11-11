# Assignment 2: An extensible text tool with a microkernel

Deadline, dates, assessment criteria and the AI policy are on Moodle. This
document describes the work itself.

## Scenario: Textwerk

Frischwerk, the grocery chain from Assignment 1, writes a lot of text: the
weekly newsletter, shelf labels, product descriptions for the web shop,
notices for the stores. The communications team prepares these texts with a
handful of scripts that nobody maintains. It wants one small tool,
*Textwerk*, that reads a text file, applies processing steps and writes the
result. Which steps will be needed next year, nobody knows.

> **Communications team:** "We need new processing steps quickly, without
> waiting for a new release of the whole tool."

> **Head of Development:** "One developer looks after the core. Plug-ins
> will be written by interns and by our agency. They must be able to do that
> from a document, without reading the core."

> **IT Operations:** "A broken plug-in must not take the tool down, and I
> want to see which plug-in caused a problem."

> **Data Protection Officer:** "A plug-in gets the text it has to process,
> and nothing else."

The Head of Development has decided on a microkernel architecture: a small
core, and everything else as plug-ins. Your group builds the proof of
concept and finds out whether the promise holds: can the tool grow without
changing the core?

## What you build

A command-line tool with a **core** in `core/` and **plug-ins** in
`plugins/`. The external behaviour is fixed in [`cli.md`](cli.md) and checked
by the acceptance tests. Everything inside is your design:

- what the core is responsible for, and what it is not,
- what a plug-in is and which interface it implements,
- how the core finds and loads plug-ins,
- what happens when a plug-in fails,
- what a plug-in may access.

You write these decisions down in [`contract.md`](contract.md), the plug-in
contract. The tool runs as a single process on one machine.

### Version 1 and version 2

- **`v1`**: the core and at least three plug-ins of your own invention. Choose
  processing steps that differ from each other; they do not have to be
  complicated.
- **`v2`**: the extension requests implemented. They are published in this
  starter repository after you have tagged `v1` (the date is on Moodle).
  You do not know them when you design your contract.

Between `v1` and `v2` you measure what each extension request changed in the
core, in the contract and in the existing plug-ins. A request that needs no
change to the core confirms your contract. A request that needs one shows
where the contract was too narrow. Both are results; the report explains
them.

### Coding agents are part of the method

Use an AI coding agent to generate the code. You write the specification
(`docs/contract.md`), the agent writes the code, and you verify what it
produced. [`AGENTS.md`](../AGENTS.md) gives the agent the repository context.
You are accountable for every line you hand in, whoever typed it.

What is assessed is your contract, your criteria, your evidence and your
reasoning. Passing the tests is necessary, but not sufficient.

## Steps

### 1. Set up

Create your group's private copy of this repository and give the lecturer
access (see the [README](../README.md#getting-started)). Run the tests once:
they all fail, because there is no core yet.

### 2. Write the plug-in contract

Fill in [`docs/contract.md`](contract.md). This is the specification you give
the agent, and the document an intern would need to write a plug-in. Be
precise: the agent will fill every gap with a guess. Commit it and tag the
commit:

```bash
git tag contract-v1
git push origin contract-v1
```

### 3. Define your criteria first

Before you generate any code, decide how you will judge your architecture
after the extension requests. Fill in [`docs/criteria.md`](criteria.md),
commit it and tag the commit `criteria-v1`.

Both tags must be older than the first commit in `core/` or `plugins/`
(apart from the README files that are already there). You may change the
contract and the criteria later, but the report must say what changed and
why.

### 4. Version 1

Generate the core and your three plug-ins with a coding agent, and provide
the two fixture directories (see [`fixtures/README.md`](../fixtures/README.md)).
Record in `ai-log/` which tool and model you used, what you gave the agent
and which prompts you used (see [`ai-log/README.md`](../ai-log/README.md)).

Verify:

```bash
make test
make conformance
```

- The **acceptance tests** check the command-line interface.
- The **conformance check** checks that the core does not know your plug-ins.

Then review the code yourselves: does it follow your contract? Does the core
do more than the contract says? Record what the agent got wrong in
`ai-log/findings.md`.

Measure what your criteria need. `make bench` gives you start-up and run
times with and without plug-ins; write your own scripts for the rest and
commit the results to `bench/results/`. Then tag:

```bash
git tag v1
git push origin v1
```

### 5. Version 2: the extension requests

When the extension requests are published, fetch them into your repository
(see the [README](../README.md#fetching-the-extension-requests)). Implement
them **one after the other, in the given order**, and tag the commit after
each one: `er1`, `er2`, `er3`. Then `make impact` reports the changes per
request.

For every request, try first to solve it with a plug-in alone. If the core
or the contract has to change, record the change in the table at the end of
`docs/contract.md`.

Verify and measure again:

```bash
make test-v2
make conformance
make impact
make bench LEVEL=v2
```

Then tag `v2`.

### 6. Assess and reflect

Fill in [`docs/report.md`](report.md): about five pages.

### 7. Submit

```bash
git tag a2-submission
git push origin --tags
```

Hand in the URL of your repository on Moodle.

## Deliverables

At the tag `a2-submission` your repository contains:

- `docs/contract.md` (tag `contract-v1`) and `docs/criteria.md` (tag
  `criteria-v1`)
- `core/`, `plugins/` and `fixtures/`, tagged `v1` and `v2`
- `ai-log/` with `findings.md`
- `bench/results/` with your measurement scripts and raw results
- `docs/report.md`
