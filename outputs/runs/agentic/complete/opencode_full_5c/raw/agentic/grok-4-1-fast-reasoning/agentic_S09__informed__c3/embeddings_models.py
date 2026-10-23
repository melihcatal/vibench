from typing import List
import re


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_texts(texts: List[str]) -> List[str]:
    return [normalize_text(t) for t in texts if normalize_text(t)]
