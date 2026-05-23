# Reviewer 1 Surgical Paper Edits

These edits address Reviewer 1's requested clarifications without changing the experimental claims.

## Addressed Issues

1. Quantization procedure was underspecified.
2. Zstandard was described as lossless, but quality dropped after using the codec pipeline.
3. COMET model/version was missing.
4. Audio segmentation procedure was not described.

## Edit 1: Introduction Method Summary

Location: Introduction, paragraph beginning "This paper studies storage-oriented post-hoc compression..."

Replace the sentence:

```text
Starting from Qwen2-Audio-7B-Instruct as a fixed backbone, the paper evaluates a simple codec-based strategy that applies quantization plus Zstandard coding only to selected transformer MLP projections, specifically gate_proj, up_proj, and down_proj, while leaving the remainder of the model unchanged.
```

with:

```text
Starting from Qwen2-Audio-7B-Instruct as a fixed backbone, the paper evaluates a simple codec-based strategy that applies a lossy weight quantization step followed by lossless Zstandard coding only to selected transformer MLP projections, specifically gate_proj, up_proj, and down_proj, while leaving the remainder of the model unchanged.
```

Why: This fixes the Zstandard ambiguity early by making clear that the pipeline is lossy because of quantization, while Zstandard itself is lossless.

## Edit 2: Task and Dataset

Location: Section 3, "Data." paragraph.

Replace:

```text
All experiments are conducted on the official English-to-Chinese evaluation split used in the shared task. The evaluation set contains 416 utterances, each paired with an English source sentence and a Chinese reference translation.
```

with:

```text
All experiments are conducted on the official English-to-Chinese evaluation split used in the shared task. The evaluation set contains 416 utterances, each paired with an English source sentence and a Chinese reference translation. We did not perform additional audio segmentation. Instead, we used the sentence-level segmented audio files distributed with the shared-task data; the local evaluation manifest points to files of the form segmented_wavs/gold/sent_*.wav.
```

Why: This directly answers the reviewer question, "How was the audio segmented for the submission?"

## Edit 3: Evaluation Setup

Location: Section 3, "Evaluation." paragraph.

Replace:

```text
Translation quality is measured with COMET, a reference-based metric in which higher scores indicate better quality.
```

with:

```text
Translation quality is measured with COMET, a reference-based metric in which higher scores indicate better quality. Specifically, we use Unbabel/wmt22-comet-da through unbabel-comet version 2.2.2 and report the system-level COMET score. COMET inputs consist of the English source text, the generated Chinese hypothesis, and the Chinese reference translation; scoring is run with batch size 16.
```

Why: This provides the missing COMET model and version, plus enough scoring detail for reproducibility.

## Edit 4: Experimental Setup

Location: Section 4, "Experimental Setup." paragraph.

Replace:

```text
The prompt is fixed to Translate this English speech into Chinese., generation uses max_new_tokens=64, and COMET is computed with the same evaluation pipeline for all runs.
```

with:

```text
The prompt is fixed to Translate this English speech into Chinese., generation uses max_new_tokens=64, and COMET is computed with the same Unbabel/wmt22-comet-da evaluation pipeline for all runs.
```

Why: This reinforces that all comparisons used the same metric pipeline.

## Edit 5: Global Codec Compression

Location: Section 4, "Global Codec Compression."

Replace the paragraph beginning:

```text
Global Codec Compression. The first custom codec-based method applies the same compression rule to all linear layers of the model.
```

through:

```text
... During inference, the compressed representation is decoded and used through a custom linear-layer wrapper.
```

with:

```text
Global Codec Compression. The first custom codec-based method applies the same compression rule to all linear layers of the model. This method is implemented with the numcodecs library, using its Quantize filter and Zstd codec. For each linear weight matrix, the tensor is detached, moved to CPU, converted to a float32 NumPy array, and encoded with a pipeline consisting of Quantize(digits=2, dtype="f4", astype="f2") followed by Zstd(level=3). The Quantize filter is the lossy stage: it rounds floating-point weights according to the requested number of significant digits and stores the quantized representation using half precision. Zstandard is then applied as a lossless entropy coder to the already-quantized byte stream. Consequently, any translation-quality degradation in this pipeline is attributable to quantization and the choice of compressed layers, not to Zstandard decompression itself. During inference, the compressed representation is decoded and used through a custom linear-layer wrapper.
```

Why: This fully answers "how does the quantization performed work?" and "what does Zstandard do?"

## Edit 6: Selected-Layer Codec Compression

Location: Section 4, "Selected-Layer Codec Compression."

Replace:

```text
All other linear layers remain unchanged. Two codec settings are considered, q2 + Zstd and q3 + Zstd, where q2 and q3 denote shorthand for Quantize(digits=2) and Quantize(digits=3), respectively.
```

with:

```text
All other linear layers remain unchanged. In Qwen2-Audio-7B-Instruct this selection yields 96 compressed linear layers. Two codec settings are considered, q2 + Zstd and q3 + Zstd, where q2 and q3 denote shorthand for Quantize(digits=2, dtype="f4", astype="f2") and Quantize(digits=3, dtype="f4", astype="f2"), respectively, both followed by Zstd(level=3).
```

Why: This adds the selected-layer count and exact q2/q3 definitions.

## Edit 7: Conclusion Wording

Location: Section 6, first paragraph.

Replace:

```text
The main focus was selected-layer codec compression, where quantization and Zstandard coding are applied only to transformer MLP projections, specifically gate_proj, up_proj, and down_proj, while the rest of the model remains unchanged.
```

with:

```text
The main focus was selected-layer codec compression, where lossy quantization followed by lossless Zstandard coding is applied only to transformer MLP projections, specifically gate_proj, up_proj, and down_proj, while the rest of the model remains unchanged.
```

Why: Keeps the conclusion aligned with the clarified method.

## Optional Author Response Text

```text
We thank the reviewer for identifying missing reproducibility details. In the revised paper, we clarify that our custom codec pipeline consists of lossy numcodecs Quantize filtering followed by lossless Zstandard compression. We now specify the exact configurations used, Quantize(digits=2 or 3, dtype="f4", astype="f2") + Zstd(level=3), the selected MLP projections compressed (gate_proj, up_proj, and down_proj), and the fact that this corresponds to 96 selected linear layers. We also clarify that quality degradation is caused by quantization and layer selection, not by Zstandard itself. Finally, we add that COMET scores were computed with Unbabel/wmt22-comet-da using unbabel-comet 2.2.2 with batch size 16, and that no additional audio segmentation was performed: the submission used the sentence-level segmented audio files provided with the shared-task data.
```
