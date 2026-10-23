import os
from typing import Optional

import deepl

from observability_models import (
    DashboardNoteTranslateRequest,
    DashboardNoteTranslateResponse,
)


def get_deepl_client() -> deepl.Translator:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError(
            "DEEPL_AUTH_KEY environment variable is required for DeepL API"
        )
    return deepl.Translator(auth_key)


def translate_dashboard_note(
    request: DashboardNoteTranslateRequest,
) -> DashboardNoteTranslateResponse:
    translator = get_deepl_client()
    target_lang = request.target_locale.upper()
    lang_map = {
        "ES": "ES",
        "FR": "FR",
        "DE": "DE",
        "JA": "JA",
        "ZH": "ZH",
        "PT": "PT-PT",
        "IT": "IT",
        "NL": "NL",
        "PL": "PL",
        "RU": "RU",
        "KO": "KO",
    }
    target = lang_map.get(target_lang, target_lang)
    source = request.source_locale.upper() if request.source_locale else None
    result = translator.translate_text(
        request.note_text,
        source_lang=source,
        target_lang=target,
    )
    return DashboardNoteTranslateResponse(
        original_text=request.note_text,
        translated_text=result.text,
        source_locale=request.source_locale,
        target_locale=request.target_locale,
        status="ok",
    )


if __name__ == "__main__":
    req = DashboardNoteTranslateRequest(
        note_text="CPU utilization exceeded 90% threshold on production hosts. Investigation required.",
        source_locale="en",
        target_locale="es",
    )
    result = translate_dashboard_note(req)
    print(f"Original: {result.original_text}")
    print(f"Translated: {result.translated_text}")
