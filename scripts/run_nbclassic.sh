#!/usr/bin/env bash
set -euo pipefail
source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate iwslt-2026
cd "$HOME/projects/iwslt2026-compression"
exec python -m nbclassic --no-browser --ip=127.0.0.1 --port=8887
