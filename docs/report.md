# Report

> About five pages. Every claim is backed by a measurement, a test result, a
> log excerpt or a reference to code. Delete the quoted guidance when you are
> done.

Group: …
Members: …

## 1. Assessment

> Three to five sentences for the Head of Development: did your plug-in
> contract hold, where did it not, and would you build on it?

## 2. Results

> One row per criterion from `criteria.md`, at `v1` and at `v2`. Link the
> evidence (file in `bench/results/`, test run, code).

| ID | Criterion | `v1` | `v2` | Evidence |
|----|-----------|------|------|----------|
| C1 | | | | |

## 3. What each extension request changed

> From `make impact` and your own observations, per extension request: files
> and lines changed in the core, changes to the contract, existing plug-ins
> that had to be adapted. For every change to the core or the contract: was
> it avoidable with a different contract, and what would that contract have
> cost at `v1`?

| Request | Core: files / lines | Contract changed? | Existing plug-ins changed | Why |
|---------|---------------------|-------------------|---------------------------|-----|
| ER1 | | | | |
| ER2 | | | | |
| ER3 | | | | |

## 4. Expectations and results

> For each criterion: what did you expect at `criteria-v1`, what did you
> measure, and if they differ, why? If you changed criteria after
> `criteria-v1`, explain it here.

## 5. Trade-offs

> What did your contract make easy, and what did it make hard? Go through
> the stakeholders: whose concern is met, whose is not.

## 6. Modular or distributed

> Your tool is one process. Name concrete conditions (a number, a
> requirement, an organisational change) under which the plug-ins would have
> to become separate services, and what would change in your contract then.
> Compare with what you saw in Assignment 1.

## 7. Limits of this proof of concept

> What does your setup not show? Think of the number of plug-ins, plug-ins
> from third parties you do not trust, the size of the texts, several users.

## 8. Reflection on working with the coding agent

> Refer to `ai-log/findings.md`. Which kinds of mistakes did the agent make?
> Which of them did the tests catch, and which only your review or your
> measurements? Did the agent respect the contract, or did it change the
> core where a plug-in would have done? What would you specify differently
> next time? What did the agent do well?
