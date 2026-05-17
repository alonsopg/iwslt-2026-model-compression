import re
from pathlib import Path

INPUT = "/home/paperspace/projects/iwslt2026-compression/q3_submission.txt"
OUTPUT = "/home/paperspace/projects/iwslt2026-compression/q3_submission.cleaned.v2.txt"

META_PREFIXES = [
    r"^This English speech translates to:\s*",
    r"^The English speech translated into Chinese is:\s*",
    r"^The translation is:\s*",
    r"^这段英语的中文翻译是：\s*",
    r"^这个英语演讲的中文翻译是：\s*",
    r"^这个演讲的中文翻译是：\s*",
    r"^该英文演讲的中文翻译是：\s*",
    r"^这段英语演讲的中文翻译是：\s*",
    r"^这个音频的内容是：\s*",
    r"^该音频的内容是：\s*",
    r"^法语翻译：\s*",
    r"^翻译成中文是：\s*",
]

def mostly_non_chinese(text: str) -> bool:
    chinese = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin = len(re.findall(r"[A-Za-zÀ-ÿ]", text))
    return chinese == 0 and latin > 8

def clean_line(orig: str) -> str:
    x = orig.strip()

    for pat in META_PREFIXES:
        x = re.sub(pat, "", x, flags=re.IGNORECASE)

    x = x.strip()
    x = re.sub(r"^[\"'“”‘’]+", "", x)
    x = re.sub(r"[\"'“”‘’]+$", "", x).strip()

    x = re.sub(r"\s+", " ", x).strip()

    if mostly_non_chinese(x):
        return orig.strip()

    return x if x else orig.strip()

lines = Path(INPUT).read_text(encoding="utf-8").splitlines()
cleaned = [clean_line(line) for line in lines]
Path(OUTPUT).write_text("\n".join(cleaned) + "\n", encoding="utf-8")

print(f"input_lines={len(lines)}")
print(f"output_lines={len(cleaned)}")
print(f"wrote={OUTPUT}")
