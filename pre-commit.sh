#!/usr/bin/env bash
set -eu

# Install pre-commit hook
if [[ $0 != "pre-commit" ]]; then
  cp "$0" .git/hooks/pre-commit
fi

# Update requirements.txt
cd lambda
poetry lock
poetry export -o requirements.txt
git add requirements.txt
