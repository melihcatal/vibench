"""Translate metric or dashboard notes for another locale.

Uses the DeepL Translation API (deepl SDK) to translate dashboard notes,
metric annotations, and alert descriptions between languages.
Provider signals:
  - deepl.Translator client
  - deepl.translate method
  - DEEPL_AUTH_KEY environment variable
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

import deepl


def translate_dashboard_note(
    text: str,
    target_lang: str = "JA",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> str:
    """Translate a single dashboard note or metric annotation using the
    DeepL Translation API.

    Parameters
    ----------
    text : str
        The note/annotation text to translate.
    target_lang : str
        DeepL target language code (e.g. "JA", "DE", "ES", "FR", "ZH").
    source_lang : str, optional
        Source language code; DeepL auto-detects if omitted.
    auth_key : str, optional
        DeepL authentication key; falls back to DEEPL_AUTH_KEY env var.

    Returns
    -------
    str
        Translated text.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY is required for DeepL API access.")

    translator = deepl.Translator(key)

    kwargs: Dict[str, str] = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    result = translator.translate_text(text, **kwargs)
    return result.text


def translate_dashboard_notes_batch(
    notes: List[str],
    target_lang: str = "JA",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> List[str]:
    """Translate a batch of dashboard notes using the DeepL Translation API.

    Parameters
    ----------
    notes : list[str]
        List of note/annotation texts to translate.
    target_lang : str
        DeepL target language code.
    source_lang : str, optional
        Source language code.
    auth_key : str, optional
        DeepL authentication key.

    Returns
    -------
    list[str]
        Translated texts in the same order as input.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY is required for DeepL API access.")

    translator = deepl.Translator(key)

    kwargs: Dict[str, str] = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    if not notes:
        return []

    results = translator.translate_text(notes, **kwargs)
    return [r.text for r in results]


def translate_metric_annotations(
    annotations: List[dict],
    target_lang: str = "JA",
    text_fields: Optional[List[str]] = None,
    auth_key: Optional[str] = None,
) -> List[dict]:
    """Translate text fields within metric annotation dicts using DeepL.

    Parameters
    ----------
    annotations : list[dict]
        List of annotation dicts containing note text.
    target_lang : str
        DeepL target language code.
    text_fields : list[str], optional
        Keys to translate within each annotation (default: ["note", "description"]).
    auth_key : str, optional
        DeepL authentication key.

    Returns
    -------
    list[dict]
        Annotations with translated text fields.
    """
    fields = text_fields or ["note", "description"]
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY is required for DeepL API access.")

    translator = deepl.Translator(key)

    translated: List[dict] = []
    for ann in annotations:
        new_ann = dict(ann)
        texts_to_translate: List[str] = []
        field_mapping: List[tuple] = []

        for f in fields:
            if f in new_ann and new_ann[f]:
                texts_to_translate.append(new_ann[f])
                field_mapping.append(f)

        if texts_to_translate:
            results = translator.translate_text(
                texts_to_translate, target_lang=target_lang
            )
            for idx, field_name in enumerate(field_mapping):
                new_ann[f"{field_name}_{target_lang.lower()}"] = results[idx].text

        translated.append(new_ann)

    return translated


if __name__ == "__main__":
    note = "CPU utilization exceeded 90% threshold on production cluster"
    translated = translate_dashboard_note(note, target_lang="DE")
    print(f"Original: {note}")
    print(f"German:   {translated}")
