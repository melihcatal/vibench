import os
import deepl
from speech_models import (
    TranslationRequest,
    TranslationResult,
    normalize_deepl_translation,
)


def translate_transcript_segments(
    segments: list,
    target_language: str = "en",
    source_language: str = None,
) -> TranslationResult:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    texts = []
    for seg in segments:
        if isinstance(seg, dict):
            texts.append(seg.get("text", seg.get("original", "")))
        else:
            texts.append(str(seg))

    translate_kwargs = {
        "target_lang": target_language.upper(),
    }
    if source_language:
        translate_kwargs["source_lang"] = source_language.upper()

    results = translator.translate_text(texts, **translate_kwargs)

    raw_segments = texts
    raw_response = [
        {"text": r.text, "detected_source_language": r.detected_source_lang}
        for r in results
    ]

    return normalize_deepl_translation(
        raw_segments, raw_response, target_language, source_language or "auto"
    )


if __name__ == "__main__":
    sample_segments = [
        {"text": "Bonjour, comment allez-vous?"},
        {"text": "Je vais bien, merci."},
    ]
    result = translate_transcript_segments(sample_segments, target_language="en")
    for seg in result.segments:
        print(f"{seg['original']} -> {seg['translated']}")
