from __future__ import annotations

import os

import deepl


def translate_transcript(segments: list[dict], target_language: str) -> dict:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("Missing DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    translated_segments = []
    for segment in segments:
        result = translator.translate_text(segment["text"], target_lang=target_language)
        translated_segments.append(
            {
                "text": result.text,
                "source_text": segment["text"],
                "speaker": segment.get("speaker"),
                "start": segment.get("start"),
                "end": segment.get("end"),
            }
        )
    return {
        "provider": "deepl",
        "target_language": target_language,
        "segments": translated_segments,
    }
