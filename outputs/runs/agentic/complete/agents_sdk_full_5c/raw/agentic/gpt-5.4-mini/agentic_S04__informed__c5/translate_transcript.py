from __future__ import annotations

import os
from typing import List

from google.cloud import translate_v2 as translate


def translate_transcript(segments: List[str], target_language: str = "es") -> List[str]:
    client = translate.Client()
    joined = [segment for segment in segments if segment]
    translated = client.translate(joined, target_language=target_language)
    if isinstance(translated, dict):
        translated = [translated]
    return [item.get("translatedText", "") for item in translated]


if __name__ == "__main__":
    raise SystemExit("import and call translate_transcript(segments)")
