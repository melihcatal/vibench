"""
dashboard_note_translate.py - Translate metric or dashboard notes for another locale.
Uses Azure AI Translator service for text translation.
Provider: Azure AI Translator
SDK: requests (REST interface to api.cognitive.microsofttranslator.com)
Auth: AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests

from observability_client import (
    DatadogConfig,
    DatadogMetricsClient,
    build_windowed_request,
)


TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
TRANSLATOR_API_VERSION = "3.0"


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    translator_key: Optional[str] = None,
    translator_region: Optional[str] = None,
) -> str:
    """
    Translate a single text string using Azure AI Translator.

    Args:
        text: The text to translate.
        target_language: Target language code (e.g. "es", "fr", "ja", "zh-Hans").
        source_language: Optional source language code (auto-detected if None).
        translator_key: Azure Translator key. Falls back to AZURE_TRANSLATOR_KEY.
        translator_region: Azure Translator region. Falls back to AZURE_TRANSLATOR_REGION.

    Returns:
        Translated text string.
    """
    translator_key = translator_key or os.environ.get("AZURE_TRANSLATOR_KEY", "")
    translator_region = translator_region or os.environ.get(
        "AZURE_TRANSLATOR_REGION", ""
    )

    if not translator_key:
        raise ValueError("AZURE_TRANSLATOR_KEY environment variable is required")
    if not translator_region:
        raise ValueError("AZURE_TRANSLATOR_REGION environment variable is required")

    url = f"{TRANSLATOR_ENDPOINT}/translate"
    params: Dict[str, str] = {
        "api-version": TRANSLATOR_API_VERSION,
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": translator_key,
        "Ocp-Apim-Subscription-Region": translator_region,
        "Content-Type": "application/json",
    }

    payload = [{"text": text}]

    response = requests.post(
        url,
        headers=headers,
        params=params,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    translation = data[0]["translations"][0]["text"]
    return translation


def translate_dashboard_notes(
    metric_name: str,
    target_language: str,
    window_minutes: int = 60,
    translator_key: Optional[str] = None,
    translator_region: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate metric notes and dashboard annotations to another locale.

    Retrieves metric data from Datadog, extracts scope and display name text
    fields that may contain dashboard notes, and translates them using
    Azure AI Translator.

    Args:
        metric_name: The Datadog metric identifier.
        target_language: Target language code (e.g. "es", "fr", "ja").
        window_minutes: Time window in minutes.
        translator_key: Azure Translator key.
        translator_region: Azure Translator region.

    Returns:
        List of dicts with original and translated text.
    """
    config = DatadogConfig()
    client = DatadogMetricsClient(config)

    request = build_windowed_request(
        metric_name=metric_name,
        window_minutes=window_minutes,
        aggregation="avg",
        rollup=60,
    )

    response = client.query(request)

    translations: List[Dict[str, Any]] = []

    for series in response.series:
        text_items = []
        if series.scope:
            text_items.append(("scope", series.scope))
        if series.display_name and series.display_name != series.metric_name:
            text_items.append(("display_name", series.display_name))

        for field_name, original_text in text_items:
            try:
                translated = translate_text(
                    original_text,
                    target_language,
                    translator_key=translator_key,
                    translator_region=translator_region,
                )
                translations.append({
                    "metric": metric_name,
                    "field": field_name,
                    "original": original_text,
                    "target_language": target_language,
                    "translated": translated,
                })
            except requests.HTTPError as exc:
                translations.append({
                    "metric": metric_name,
                    "field": field_name,
                    "original": original_text,
                    "target_language": target_language,
                    "translated": None,
                    "error": str(exc),
                })

    return translations


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: dashboard_note_translate.py <metric_name> <target_language> "
            "[--window MINUTES]"
        )
        sys.exit(1)

    metric_name = sys.argv[1]
    target_language = sys.argv[2]
    window = 60

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--window" and i + 1 < len(sys.argv):
            window = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    translations = translate_dashboard_notes(
        metric_name, target_language, window
    )

    print(json.dumps(translations, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
