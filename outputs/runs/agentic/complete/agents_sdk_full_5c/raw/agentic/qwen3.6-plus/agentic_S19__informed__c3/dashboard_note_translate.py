"""Translate metric or dashboard notes for another locale.

Uses DeepL API (deepl SDK) to translate dashboard annotations,
metric descriptions, or alert notes into a target language.

Required environment:
    DEEPL_AUTH_KEY - DeepL API authentication key
"""

from __future__ import annotations

import json
import os
from typing import List, Optional

import deepl

from observability_client import ObservabilityClient
from observability_models import MetricSeries


def extract_dashboard_notes(
    series_list: List[MetricSeries],
) -> List[str]:
    """Extract text notes and descriptions from metric metadata."""
    notes = []
    for s in series_list:
        for key, value in s.resource_labels.items():
            if "description" in key.lower() or "note" in key.lower():
                if isinstance(value, str) and len(value) > 0:
                    notes.append(value)
        for key, value in s.metric_labels.items():
            if "description" in key.lower() or "note" in key.lower():
                if isinstance(value, str) and len(value) > 0:
                    notes.append(value)
    return notes


def translate_notes(
    notes: List[str],
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
    deepl_auth_key: Optional[str] = None,
) -> List[dict]:
    """Translate a list of notes using DeepL API.

    Args:
        notes: List of text strings to translate
        target_lang: DeepL target language code (e.g. ES, FR, DE, JA)
        source_lang: Optional source language code
        deepl_auth_key: DeepL auth key (falls back to DEEPL_AUTH_KEY env var)

    Returns:
        List of dicts with original text, translated text, and detected source lang.
    """
    auth_key = deepl_auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY must be set")

    translator = deepl.Translator(auth_key)

    translations = []
    for note in notes:
        if not note.strip():
            continue

        result = translator.translate_text(
            note,
            target_lang=target_lang,
            source_lang=source_lang,
        )

        translations.append({
            "original": note,
            "translated": result.text,
            "detected_source_lang": result.detected_source_lang,
            "target_lang": target_lang,
        })

    return translations


def translate_dashboard_notes(
    metric_type: str,
    target_lang: str = "ES",
    project_id: Optional[str] = None,
    minutes: int = 60,
    deepl_auth_key: Optional[str] = None,
) -> List[dict]:
    """Translate dashboard notes associated with a metric.

    Retrieves metric data from Google Cloud Monitoring, extracts
    text labels/notes, and translates them using DeepL API.
    """
    client = ObservabilityClient(project_id=project_id)
    series_list = client.query_metric_window(metric_type, minutes=minutes)

    notes = extract_dashboard_notes(series_list)
    if not notes:
        return [{"status": "no_notes_found", "metric_type": metric_type}]

    return translate_notes(notes, target_lang=target_lang, deepl_auth_key=deepl_auth_key)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Translate dashboard notes via DeepL API")
    parser.add_argument("--metric-type", required=True, help="GCP metric type")
    parser.add_argument("--project-id", default=None)
    parser.add_argument("--target-lang", default="ES", help="Target language code")
    parser.add_argument("--minutes", type=int, default=60)
    args = parser.parse_args()

    translations = translate_dashboard_notes(
        metric_type=args.metric_type,
        target_lang=args.target_lang,
        project_id=args.project_id,
        minutes=args.minutes,
    )
    print(json.dumps(translations, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
