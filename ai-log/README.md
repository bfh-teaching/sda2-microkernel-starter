# AI log

Record how you worked with coding agents, so that someone else can follow
what was generated, from which input, and what you changed.

## What to record

Create one file per step: `ai-log/v1.md` for the core and your plug-ins, and
`ai-log/v2.md` for the extension requests, with:

| Field | Example |
|-------|---------|
| Tool | e.g. Claude Code, Codex, Cursor, GitHub Copilot |
| Model and version | as shown by the tool |
| Date(s) | |
| Who drove the session | |
| Input given | the versions of `docs/contract.md` and other files (commit hash) |
| Prompts | the prompts in the order you used them, verbatim |
| Manual changes | what you changed by hand afterwards, with commit hashes |

Exported transcripts are welcome: put them next to the file, for example
`ai-log/v1-session-1.md`. Remove secrets and personal data first.

If you also used AI for other parts (contract, criteria, report), say where
and how in the same way, in `ai-log/other.md`.

## Findings

Everything the agent got wrong or did in a risky way goes into
[`findings.md`](findings.md), including what you found before the tests did.
A short list of real findings is worth more than a long list of trivial ones.
