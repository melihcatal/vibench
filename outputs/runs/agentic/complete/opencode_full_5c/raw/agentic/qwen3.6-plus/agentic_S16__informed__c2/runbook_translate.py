import os
import json
import deepl
from security_models import TranslationResult


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
translator = deepl.Translator(DEEPL_AUTH_KEY)


def translate_runbook_notes(
    source_text: str,
    target_language: str = "EN-US",
    source_language: str = None,
) -> TranslationResult:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DeepL API key not configured")
    kwargs = {}
    if source_language:
        kwargs["source_lang"] = source_language
    result = translator.translate_text(
        source_text,
        target_lang=target_language,
        **kwargs,
    )
    detected_source = (
        result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else source_language or "AUTO"
    )
    return TranslationResult(
        source_text=source_text,
        translated_text=result.text,
        source_language=detected_source,
        target_language=target_language,
        provider="DeepL API",
    )


def translate_multiple_runbook_notes(
    notes_list: list,
    target_language: str = "EN-US",
    source_language: str = None,
) -> list:
    results = []
    for notes in notes_list:
        results.append(translate_runbook_notes(notes, target_language, source_language))
    return results


if __name__ == "__main__":
    test_notes = os.environ.get(
        "RUNBOOK_NOTES",
        "Schritt 1: Generieren Sie ein neues Geheim. Schritt 2: Aktualisieren Sie die Anwendungskonfiguration.",
    )
    result = translate_runbook_notes(test_notes, target_language="EN-US")
    print(json.dumps(result.to_dict(), indent=2))
