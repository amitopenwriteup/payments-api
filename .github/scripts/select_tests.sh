#!/bin/bash
# Heuristic test selector — Part 3 fallback (no Launchable token required).
# Finds test files that import any of the Python source files changed in this PR.

set -euo pipefail

BASE_REF="${BASE_REF:-main}"

CHANGED_FILES=$(git diff --name-only "origin/${BASE_REF}...HEAD" -- '*.py' \
  | grep -v '^tests/' \
  | sed 's|app/||; s|\.py$||; s|/|.|g' || true)

if [ -z "$CHANGED_FILES" ]; then
  echo "No source files changed — running full suite" >&2
  echo "tests/"
  exit 0
fi

echo "Changed modules: $CHANGED_FILES" >&2
SELECTED=""

for module in $CHANGED_FILES; do
  matches=$(grep -rl "from app\.${module}\|import ${module}" tests/ 2>/dev/null || true)
  SELECTED="$SELECTED $matches"
done

SELECTED=$(echo "$SELECTED" | tr ' ' '\n' | sort -u | tr '\n' ' ' | xargs)

if [ -z "$SELECTED" ]; then
  echo "No impacted tests found — running full suite as fallback" >&2
  echo "tests/"
else
  echo "Impacted tests: $SELECTED" >&2
  echo "$SELECTED"
fi
