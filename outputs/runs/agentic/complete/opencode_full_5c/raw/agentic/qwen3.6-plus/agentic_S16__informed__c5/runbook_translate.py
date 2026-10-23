import os
from typing import Optional
import deepl
from security_models import RunbookNote


def translate_runbook_note(
    source_text: str,
    target_language: str = "en",
    source_language: str = None,
    auth_key: str = None,
) -> str:
    auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(auth_key)
    kwargs = {"target_lang": target_language.upper()}
    if source_language:
        kwargs["source_lang"] = source_language.upper()
    result = translator.translate_text(source_text, **kwargs)
    return result.text


def translate_runbook_notes_batch(
    notes: list,
    target_language: str = "en",
    source_language: str = None,
    auth_key: str = None,
) -> list:
    auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(auth_key)
    texts = []
    for note in notes:
        if isinstance(note, RunbookNote):
            texts.append(note.source_text)
        elif isinstance(note, str):
            texts.append(note)
        elif isinstance(note, dict):
            texts.append(note.get("text", note.get("source_text", "")))
    kwargs = {"target_lang": target_language.upper()}
    if source_language:
        kwargs["source_lang"] = source_language.upper()
    results = translator.translate_text(texts, **kwargs)
    translated = []
    for i, note in enumerate(notes):
        if isinstance(note, RunbookNote):
            note.translated_text = results[i].text
            translated.append(note)
        elif isinstance(note, str):
            translated.append(results[i].text)
        elif isinstance(note, dict):
            translated.append(
                {
                    **note,
                    "translated_text": results[i].text,
                }
            )
    return translated


def process_runbook_with_metadata(
    runbook: RunbookNote,
    auth_key: str = None,
) -> RunbookNote:
    auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY environment variable is required")
    translator = deepl.Translator(auth_key)
    kwargs = {"target_lang": runbook.target_language.upper()}
    if runbook.source_language:
        kwargs["source_lang"] = runbook.source_language.upper()
    result = translator.translate_text(runbook.source_text, **kwargs)
    runbook.translated_text = result.text
    return runbook


if __name__ == "__main__":
    sample_text = (
        "Die Rotation des Datenbank-Passworts wurde erfolgreich abgeschlossen."
    )
    result = translate_runbook_note(
        sample_text, target_language="en", source_language="de"
    )
    print(f"Original: {sample_text}")
    print(f"Translated: {result}")
