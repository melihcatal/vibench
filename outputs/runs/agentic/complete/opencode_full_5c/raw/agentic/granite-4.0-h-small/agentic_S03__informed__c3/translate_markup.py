from __future__ import annotations

import os
import sys

from translation_client import load_auth_token, normalize_request, get_provider_config
from translation_models import MarkupTranslateRequest, MarkupTranslateResponse

# Map of provider name to entrypoint function (stubbed here)
PROVIDERS = {
    "deepl": "translate_markup_deepl",
    "google": "translate_markup_google",
    "azure": "translate_markup_azure",
    "amazon": "translate_markup_amazon",
    "alibaba": "translate_markup_alibaba",
}


def translate_markup(
    html: str,
    source_lang: str,
    target_lang: str,
    provider: str = "deepl",
) -> MarkupTranslateResponse:
    """
    Translate HTML/markup text while preserving tags and structure.

    Args:
        html: Source HTML/markup string.
        source_lang: ISO 639-1 source language code.
        target_lang: ISO 639-1 target language code.
        provider: One of the supported providers.

    Returns:
        MarkupTranslateResponse with translated_html field.
    """
    if provider not in PROVIDERS:
        raise ValueError(
            f"Unsupported provider: {provider}. Choose from {list(PROVIDERS)}"
        )

    auth_token = load_auth_token(provider)
    cfg = get_provider_config(provider)
    payload = normalize_request(
        {"html": html, "source_lang": source_lang, "target_lang": target_lang}, provider
    )
    # The concrete provider stubs will handle HTML‑aware translation (e.g., preserve tags)
    result = globals()[PROVIDERS[provider]](auth_token, payload)
    return result


# --------------------------------------------------------------------
# Concrete provider stubs (replace with real SDK/HTML‑aware integration)
# --------------------------------------------------------------------
def translate_markup_deepl(auth: str, payload: dict) -> MarkupTranslateResponse:
    return MarkupTranslateResponse(
        translated_html=f"[DeePL] HTML preserved, translated text in `{payload['target_lang']}`"
    )


def translate_markup_google(auth: str, payload: dict) -> MarkupTranslateResponse:
    return MarkupTranslateResponse(
        translated_html=f"[Google] HTML preserved, translated text in `{payload['target_lang']}`"
    )


def translate_markup_azure(auth: str, payload: dict) -> MarkupTranslateResponse:
    return MarkupTranslateResponse(
        translated_html=f"[Azure] HTML preserved, translated text in `{payload['target_lang']}`"
    )


def translate_markup_amazon(auth: str, payload: dict) -> MarkupTranslateResponse:
    return MarkupTranslateResponse(
        translated_html=f"[Amazon] HTML preserved, translated text in `{payload['target_lang']}`"
    )


def translate_markup_alibaba(auth: str, payload: dict) -> MarkupTranslateResponse:
    return MarkupTranslateResponse(
        translated_html=f"[Alibaba] HTML preserved, translated text in `{payload['target_lang']}`"
    )


# --------------------------------------------------------------------
# CLI helper for manual testing
# --------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print(
            f'Usage: {sys.argv[0]} "<html>" <source_lang> <target_lang> <provider>\nProvider choices: {", ".join(PROVIDERS)}'
        )
        sys.exit(1)
    _, raw_html, src, tgt, prov = sys.argv
    result = translate_markup(raw_html, src, tgt, prov)
    print(result["translated_html"])
