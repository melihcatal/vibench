import os
import deepl
from typing import Dict, Optional


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")


def translate_compliance_note(
    text: str,
    target_language: str = "EN",
    source_language: Optional[str] = None,
) -> Dict:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(DEEPL_AUTH_KEY)

    translate_kwargs = {}
    if source_language:
        translate_kwargs["source_lang"] = source_language
    translate_kwargs["target_lang"] = target_language

    result = translator.translate_text(text, **translate_kwargs)

    return {
        "translated_text": result.text,
        "detected_source_language": result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else "",
        "confidence": 1.0,
        "request_id": "",
    }


def translate_batch_compliance_notes(
    texts: list,
    target_language: str = "EN",
    source_language: Optional[str] = None,
) -> Dict:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(DEEPL_AUTH_KEY)

    translate_kwargs = {}
    if source_language:
        translate_kwargs["source_lang"] = source_language
    translate_kwargs["target_lang"] = target_language

    results = translator.translate_text(texts, **translate_kwargs)

    translated_texts = []
    for r in results:
        translated_texts.append(r.text)

    return {
        "translated_texts": translated_texts,
        "detected_source_language": results[0].detected_source_lang
        if results and hasattr(results[0], "detected_source_lang")
        else "",
        "confidence": 1.0,
        "request_id": "",
    }


if __name__ == "__main__":
    sample_note = "Die Verschlusselung wurde gemass DSGVO-Anforderungen aktualisiert."
    result = translate_compliance_note(sample_note, target_language="EN")
    print(result)
