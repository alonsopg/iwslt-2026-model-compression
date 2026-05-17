#!/usr/bin/env bash
set -euo pipefail
source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate iwslt-2026
python - <<'PY'
import torch
print("torch:", torch.__version__)
print("cuda:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("gpu:", torch.cuda.get_device_name(0))
import bitsandbytes as bnb
print("bitsandbytes:", bnb.__version__)
PY
python -m bitsandbytes || true
