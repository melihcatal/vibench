"""
compliance_note_translate.py - Translate encryption or compliance notes for reviewers using DeepL API.

Uses DeepL Translation API via deepl SDK.
Provider signals: deepl SDK import, DEEPL_AUTH_KEY auth,
api.deepl.com endpoint, DeepL model/service identifiers.
"""

import os
from typing import Dict, List, Optional, Any

import deepl


def get_deepl_client(auth_key: Optional[str] = None) -> deepl.Translator:
    """
    Create a DeepL translator client using DEEPL_AUTH_KEY environment variable.
    Connects to the DeepL API at api.deepl.com.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    translator = deepl.Translator(key)
    return translator


def translate_compliance_note(
    text: str,
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a compliance or encryption note using DeepL Translation API.

    DeepL provider: Uses the DeepL API at api.deepl.com
    via the deepl Python SDK. Supports formality and source language hints.
    """
    translator = get_deepl_client()

    translate_kwargs: Dict[str, Any] = {
        "target_lang": target_lang,
    }

    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    if formality:
        translate_kwargs["formality"] = formality

    result = translator.translate_text(text, **translate_kwargs)

    return {
        "translated_text": result.text,
        "source_lang": result.detected_source_lang,
        "target_lang": target_lang,
        "original_text": text,
        "provider": "DeepL Translation API (api.deepl.com)",
    }


def translate_compliance_notes_batch(
    texts: List[str],
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate multiple compliance notes in a batch using DeepL.

    DeepL provider: Uses the DeepL API at api.deepl.com
    with the deepl Python SDK. DeepL supports batch translation
    in a single API call.
    """
    translator = get_deepl_client()

    translate_kwargs: Dict[str, Any] = {
        "target_lang": target_lang,
    }

    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    results = translator.translate_text(texts, **translate_kwargs)

    translated_list = []
    for i, result in enumerate(results):
        translated_list.append({
            "translated_text": result.text,
            "source_lang": result.detected_source_lang,
            "target_lang": target_lang,
            "original_text": texts[i] if i < len(texts) else "",
            "provider": "DeepL Translation API (api.deepl.com)",
        })

    return translated_list


def translate_audit_report(
    report_text: str,
    target_language: str = "EN-US",
    include_metadata: bool = True,
) -> Dict[str, Any]:
    """
    Translate a full audit report for international reviewers using DeepL.

    DeepL provider: Uses the DeepL API at api.deepl.com.
    The deepl SDK handles text translation with proper language detection.
    """
    translator = get_deepl_client()

    result = translator.translate_text(
        report_text,
        target_lang=target_language,
    )

    output: Dict[str, Any] = {
        "translated_text": result.text,
        "source_lang": result.detected_source_lang,
        "target_lang": target_language,
        "provider": "DeepL Translation API (api.deepl.com)",
    }

    if include_metadata:
        output["original_length"] = len(report_text)
        output["translated_length"] = len(result.text)

    return output


def translate_for_review(
    notes: List[str],
    reviewer_language: str = "EN-US",
) -> Dict[str, Any]:
    """
    Translate compliance/encryption notes for reviewers in their preferred language.
    Uses DeepL batch translation via api.deepl.com.
    """
    translations = translate_compliance_notes_batch(
        texts=notes,
        target_lang=reviewer_language,
    )

    return {
        "translations": translations,
        "note_count": len(translations),
        "reviewer_language": reviewer_language,
        "provider": "DeepL Translation API (api.deepl.com)",
    }


if __name__ == "__main__":
    sample_note = "Die Schlüsselrotation wurde am 15. Januar 2024 für die Produktionsumgebung abgeschlossen."

    try:
        result = translate_compliance_note(
            text=sample_note,
            target_lang="EN-US",
        )
        print(f"Original: {result['original_text']}")
        print(f"Detected source: {result['source_lang']}")
        print(f"Translation: {result['translated_text']}")
        print(f"Provider: {result['provider']}")
    except ValueError as e:
        print(f"Error: {e}")
        print("Set DEEPL_AUTH_KEY environment variable to run translation.")
