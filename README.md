# IWSLT 2026 Model Compression Experiments

Notebook-driven experiments for compressing and evaluating [`Qwen/Qwen2-Audio-7B-Instruct`](https://huggingface.co/Qwen/Qwen2-Audio-7B-Instruct) on the IWSLT 2026 speech translation/model compression workflow.

The repository keeps the code, notebooks, manifests, submission text files, and lightweight experiment summaries in Git. Large datasets, model checkpoints, compressed model artifacts, and archives are intentionally excluded because they are stored externally on Hugging Face.

## Repository Layout

```text
.
├── notebooks/              # Main experiment notebooks
├── scripts/                # Environment/GPU sanity-check helpers
├── data/manifests/         # Committed dev/eval manifests
├── outputs/reports/        # Consolidated result tables
├── outputs/experiment_results/
│   └── */                  # Lightweight predictions, summaries, policies
├── outputs-backup/         # Backup summaries and historical result tables
├── clean_q3_submission*.py # Submission cleanup utilities
└── *_submission*.txt       # Generated submission hypotheses
```

Ignored local-only paths include `data/raw/`, `data/test_sets/`, `outputs/submission_artifacts/`, model artifact folders, checkpoints, and compressed archives.

## Main Entry Points

- `notebooks/model-compression-V1.ipynb` and `notebooks/model-compression-V1-Copy2.ipynb`: model compression exploration.
- `notebooks/01_qwen2audio_comet_en_zh-*.ipynb`: Qwen2-Audio evaluation and COMET scoring runs.
- `notebooks/Selected-layer codec compression.ipynb`: selected-layer codec experiments.
- `notebooks/Selected-Layer Codec Compression with q3 + Zstd.ipynb`: q3 + Zstd selected-layer codec run.
- `notebooks/prunning-only-exp.ipynb`: pruning-only experiment.
- `notebooks/table.ipynb`: result table generation.
- `notebooks/submissions.ipynb`: submission artifact preparation.

## Environment

The original experiments used a conda environment named `iwslt-2026`.

```bash
conda activate iwslt-2026
```

Useful checks:

```bash
scripts/check_gpu.sh
scripts/check_bnb.sh
```

To start the notebook server used in this workspace:

```bash
scripts/run_nbclassic.sh
```

That launches nbclassic on `127.0.0.1:8887`.

## Results

The most useful summary tables are:

- `outputs/reports/paper_results_table_compact_display.csv`
- `outputs/reports/paper_results_table_clean_display.csv`
- `outputs/reports/all_experiment_results_table.csv`
- `outputs/reports/best_per_experiment_run_split.csv`

The compact display table includes COMET, delta versus baseline, seconds per item, compression ratio, and estimated original/compressed size.

## Submission Files

The root-level submission files are retained for reproducibility:

- `int8_submission.txt`
- `global_q2_submission.txt`
- `q3_submission.txt`
- `q3_submission.cleaned.txt`
- `q3_submission.cleaned.v2.txt`
- `q3_submission.cleaned.v3.txt`

The `clean_q3_submission.py` and `clean_q3_submission_v2.py` scripts remove common model preambles and quote noise from q3 submission hypotheses.

## External Artifacts

Large artifacts are not committed to Git:

- raw ACL/IWSLT data
- local test bundles
- `.pt`, `.bin`, `.safetensors`, `.ckpt`, and similar checkpoint files
- compressed model archives and submission artifacts
- model artifact directories under `outputs/experiment_results/**/model_artifacts/`

Those files are expected to be restored from the Hugging Face artifact storage used for these experiments before rerunning notebooks that depend on local checkpoints or raw audio.

Relevant Hugging Face model/artifact repositories:

- [`Qwen/Qwen2-Audio-7B-Instruct`](https://huggingface.co/Qwen/Qwen2-Audio-7B-Instruct): upstream baseline model used by the experiments.
- [`alonsopg/qwen2audio-selected-layer-codec-q2`](https://huggingface.co/alonsopg/qwen2audio-selected-layer-codec-q2): selected-layer custom codec artifact with q2 quantization and Zstd.
- [`alonsopg/qwen2audio-selected-layer-codec-q3`](https://huggingface.co/alonsopg/qwen2audio-selected-layer-codec-q3): selected-layer custom codec artifact with q3 quantization and Zstd.

Example artifact restore commands:

```bash
huggingface-cli download alonsopg/qwen2audio-selected-layer-codec-q2 \
  --local-dir outputs/submission_artifacts/selected_layer_codec_q2_zstd

huggingface-cli download alonsopg/qwen2audio-selected-layer-codec-q3 \
  --local-dir outputs/submission_artifacts/selected_layer_codec_q3_zstd
```

## Git Notes

This repo is configured to keep Git lightweight. If new experiments create large files, leave them out of Git and place them in the external artifact store instead.
