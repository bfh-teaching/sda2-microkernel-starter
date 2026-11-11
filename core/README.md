# core/

Your core goes here. It must be startable as described in
[`docs/cli.md`](../docs/cli.md) (by default `python3 -m core`, so a Python
core needs `core/__main__.py`).

The core must not know any plug-in by name and must not import a plug-in
statically. `make conformance` checks both.
