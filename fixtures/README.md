# fixtures/

Two plug-in directories that the acceptance tests use to check how your core
deals with faulty plug-ins. You provide them, in the form of your contract.
The tests start the tool with `TEXTWERK_PLUGINS` pointing at one of them.

| Directory | Must contain |
|---|---|
| `broken-load/` | at least one working plug-in, and one plug-in that cannot be loaded (for example a syntax error, or a plug-in that violates your contract) |
| `broken-run/` | a plug-in with the name `boom` that loads and is listed, but always fails when it processes a text |

The working plug-in in `broken-load/` may be a copy of one of yours.
