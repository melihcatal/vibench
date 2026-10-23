from __future__ import annotations

from typing import Any, Dict, List

from deepl import Translator

from speech_client import load_config


def translate_transcript(segments: List[Dict[str, Any]], target_language: str = "EN-US") -> Dict[str, Any]:
    auth_key = load_config().api_key
    translator = Translator(auth_key)  # provider-identifying DeepL SDK
    texts = [segment.get("text", "") for segment in segments if segment.get("text")]
    translated = translator.translate_text(texts, target_lang=target_language)
    results = []
    if isinstance(translated, list):
        iterable = translated
    else:
        iterable = [translated]
    for segment, item in zip(segments, iterable):
        results.append({**segment, "translated_text": item.text})
    return {"provider": "DeepL", "target_language": target_language, "segments": results}
