from __future__ import annotations

import os
from typing import Dict, List, Sequence

import deepl


def translate_transcript(
    segments: Sequence[Dict[str, str]],
    target_language: str,
    source_language: str | None = None,
) -> List[Dict[str, str]]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    texts = [segment.get("text", "") for segment in segments]
    results = translator.translate_text(texts, target_lang=target_language, source_lang=source_language)
    if not isinstance(results, list):
        results = [results]
    output: List[Dict[str, str]] = []
    for segment, result in zip(segments, results):
        item = dict(segment)
        item["translated_text"] = result.text
        item["detected_source_language"] = result.detected_source_lang
        output.append(item)
    return output
