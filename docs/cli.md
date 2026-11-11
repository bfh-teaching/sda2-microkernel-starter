# Command-line interface (binding)

This is the external behaviour of the tool. The acceptance tests check it
from the outside. How the core and the plug-ins work together inside is your
design: you define it in [`contract.md`](contract.md).

## Starting the tool

The tool is started from the repository root. The default command is

```bash
python3 -m core
```

If your tool starts differently (another language, a wrapper script), set the
environment variable `TEXTWERK_CMD` to your command before you run the tests,
for example `TEXTWERK_CMD="node core/main.js"`.

Below, `textwerk` stands for this command.

## Commands

### `textwerk list`

Prints the available plug-ins to standard output, one per line, sorted by
name:

```
<name><TAB><description>
```

- A plug-in name starts with a lowercase letter and consists of lowercase
  letters, digits and hyphens; it has at least three characters. Names are
  unique.
- The description is one line of free text and is not empty.
- Without any plug-in, nothing is printed.
- Exit code `0`.

### `textwerk run --input IN --output OUT [--plugin NAME]...`

Reads the text file `IN` (UTF-8), applies the named plug-ins in the order
given, and writes the result to `OUT` (UTF-8).

- `--plugin` may be given several times, also with the same name.
- Without `--plugin`, `OUT` is a byte-identical copy of `IN`.
- Exit code `0`.

## Errors

| Situation | Exit code | Standard error |
|---|---|---|
| Wrong usage, or `IN` does not exist or cannot be read | `2` | a message |
| A name given with `--plugin` is not an available plug-in | `3` | a message that contains the name |
| A plug-in fails while it processes the text | `4` | a message that contains the name of the plug-in |

In all three cases `OUT` is neither created nor changed, and the message is
written for a user: no stack trace.

## Where plug-ins come from

Plug-ins are found at run time in the directory `plugins/`. If the
environment variable `TEXTWERK_PLUGINS` is set, the tool searches that
directory instead. An empty or missing directory means: no plug-ins.

A plug-in that cannot be loaded must not stop the tool: `textwerk list` still
lists the other plug-ins and ends with exit code `0`, and a warning on
standard error tells the user which plug-in was skipped.

## Fixtures you provide

The tests need two plug-in directories with faulty plug-ins, written in the
form of your contract: see [`../fixtures/README.md`](../fixtures/README.md).

## What the conformance check looks at

`make conformance` reads the files in `core/`:

- No file in `core/` contains the name of one of your plug-ins (as listed by
  `textwerk list`). The core finds plug-ins; it does not know them. Choose
  distinctive plug-in names, so that a name is not an ordinary word in your
  core.
- No file in `core/` imports from `plugins` statically.
