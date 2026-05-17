import re
from pathlib import Path

INPUT = "/home/paperspace/projects/iwslt2026-compression/q3_submission.txt"
OUTPUT = "/home/paperspace/projects/iwslt2026-compression/q3_submission.cleaned.txt"

META_PREFIXES = [
    r"^This English speech translates to:\s*",
    r"^The English speech translated into Chinese is:\s*",
    r"^The translation is:\s*",
    r"^这段英语的中文翻译是：\s*",
    r"^这个英语演讲的中文翻译是：\s*",
    r"^该英文演讲的中文翻译是：\s*",
    r"^这段英语演讲的中文翻译是：\s*",
    r"^这个音频的内容是：\s*",
    r"^该音频的内容是：\s*",
    r"^法语翻译：\s*",
    r"^翻译成中文是：\s*",
]

def clean_line(line: str) -> str:
    orig = line.rstrip("\n")
    x = orig.strip()

    for pat in META_PREFIXES:
        x = re.sub(pat, "", x, flags=re.IGNORECASE)

    x = re.sub(r'^[\"“”‘’\']+', "", x)
    x = re.sub(r'[\"“”‘’\']+$', "", x).strip()

    if re.match(r"^[A-Za-z][A-Za-z ,:'()/-]{8,}", x):
        m = re.search(r"[\u4e00-\u9fff].*", x)
        if m:
            x = m.group(0).strip()

    x = re.sub(r"\s+", " ", x).strip()

    if not x:
        x = orig.strip()

    return x

lines = Path(INPUT).read_text(encoding="utf-8").splitlines()
cleaned = [clean_line(line) for line in lines]
Path(OUTPUT).write_text("\n".join(cleaned) + "\n", encoding="utf-8")

print(f"input_lines={len(lines)}")
print(f"output_lines={len(cleaned)}")
print(f"wrote={OUTPUT}")
