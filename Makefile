# Textwerk starter: tests and measurements. Needs Python 3.10+ and git.
# Without make, run the python commands below directly
# (on Windows usually "python" instead of "python3").

PY ?= python3
LEVEL ?= v1

.PHONY: test test-v2 conformance bench impact

test:
	$(PY) -m unittest discover -s tests/acceptance -v

test-v2: test
	@test -d tests/er || (echo "tests/er not found: fetch the extension requests first (see README)"; exit 1)
	$(PY) -m unittest discover -s tests/er -v

conformance:
	$(PY) -m unittest discover -s tests/conformance -v

bench:
	$(PY) bench/measure.py $(LEVEL)

impact:
	$(PY) bench/change_impact.py
