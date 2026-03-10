#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ ! -x ".venv/bin/python" ]; then
  echo "Virtual environment not found. Running setup..."
  bash ./setup.sh
fi

exec ".venv/bin/python" main.py "$@"
