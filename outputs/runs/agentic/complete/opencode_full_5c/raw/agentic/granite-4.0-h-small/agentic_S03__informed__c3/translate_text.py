from __future__ import annotations

import os
import sys

from translation_client import load_auth_token, normalize_request, get_provider_config
from translation_models import TranslateRequest, TranslateResponse

# Map of provider name to entrypoint function (stubbed here)
PROVIDERS = {
    "deepl": "translate_deepl",
    "google": "translate_google",
    "azure": "translate_azure",
    "amazon": "translate_amazon",
    "alibaba": "translate_alibaba",
}


def translate_text(
    text: str,
    source_lang: str,
    target_lang: str,
    provider: str = "deepl",
) -> TranslateResponse:
    """
    Translate a single string using the selected provider.

    Args:
        text: The source text.
        source_lang: ISO 639-1 source language code (e.g., 'en').
        target_lang: ISO 639-1 target language code (e.g., 'es').
        provider: One of 'deepl','google','azure','amazon','alibaba'.
            Defaults to 'deepl'.

    Returns:
        A TranslateResponse dict with translated_text and language fields.
    """
    if provider not in PROVIDERS:
        raise ValueError(
            f"Unsupported provider: {provider}. Choose from {list(PROVIDERS)}"
        )

    # Load credentials for the chosen provider
    auth_token = load_auth_token(provider)

    # Configure provider‑specific parameters (e.g., endpoint, model)
    cfg = get_provider_config(provider)
    # For simplicity we just pass the token; actual SDK init would use it
    # Example: client = DeepLClient(auth=auth_token)  # this import is hidden

    # Normalize the generic request to the provider's shape
    payload = normalize_request(
        {"text": text, "source_lang": source_lang, "target_lang": target_lang}, provider
    )

    # Call the concrete provider function (these are imported lazily below)
    translated = globals()[PROVIDERS[provider]](auth_token, payload)

    # Cast to the generic response type
    return translated


# --------------------------------------------------------------------
# Concrete provider implementations (stubs that would call the real SDK)
# --------------------------------------------------------------------
def translate_deepl(auth: str, payload: dict) -> TranslateResponse:
    """Stub for DeepL SDK call."""
    # from deep import translate  # actual import would be: import deepl; deepl_client = deepl.create_client(auth=auth)
    # result = deepl_client.translate_text(**payload)
    # return TranslateResponse(translated_text=result['text'], source_lang=payload['source_lang'], target_lang=payload['target_lang'])
    return TranslateResponse(
        translated_text=f"[DeePL] '{payload['text']}' → {payload['target_lang']}",
        source_lang=payload["source_lang"],
        target_lang=payload["target_lang"],
    )


def translate_google(auth: str, payload: dict) -> TranslateResponse:
    """Stub for Google Cloud Translation call."""
    # from google.cloud import translate_v2 as translate
    # client = translate.Client(credentials=auth)
    # result = client.translate(payload['text'], source_language=payload['source_lang'], target_language=payload['target_lang'])
    return TranslateResponse(
        translated_text=f"[Google] '{payload['text']}' → {payload['target_lang']}",
        source_lang=payload["source_lang"],
        target_lang=payload["target_lang"],
    )


def translate_azure(auth: str, payload: dict) -> TranslateResponse:
    """Stub for Azure AI Translator call."""
    # from azure.ai.translation.text import TextTranslationClient, ModelInfo
    # client = TextTranslationClient(endpoint=\"https://<region>.translator.azure.net\", credential=auth)
    # result = client.translate(texts=[payload['text']], source_language=payload['source_lang'], target_language=payload['target_lang'])
    return TranslateResponse(
        translated_text=f"[Azure] '{payload['text']}' → {payload['target_lang']}",
        source_lang=payload["source_lang"],
        target_lang=payload["target_lang"],
    )


def translate_amazon(auth: str, payload: dict) -> TranslateResponse:
    """Stub for Amazon Translate call."""
    # import boto3
    # client = boto3.client('translate', region_name=..., aws_access_key_id=..., aws_secret_access_key=...)
    # result = client.TranslateText(Text=payload['text'], SourceLanguageCode=payload['source_lang'], TargetLanguageCode=payload['target_lang'])
    return TranslateResponse(
        translated_text=f"[Amazon] '{payload['text']}' → {payload['target_lang']}",
        source_lang=payload["source_lang"],
        target_lang=payload["target_lang"],
    )


def translate_alibaba(auth: str, payload: dict) -> TranslateResponse:
    """Stub for Alibaba Cloud Machine Translation call."""
    # from aliyun.openapi import client as AcsClient
    # client = AcsClient(access_key_id=..., access_key_secret=...)
    # result = client.get_response('TranslateText', payload)
    return TranslateResponse(
        translated_text=f"[Alibaba] '{payload['text']}' → {payload['target_lang']}",
        source_lang=payload["source_lang"],
        target_lang=payload["target_lang"],
    )


# --------------------------------------------------------------------
# Helper to print usage when script is executed directly
# --------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            f"Usage: {sys.argv[0]} <text> <source_lang> <target_lang> <provider>\nProvider choices: {', '.join(PROVIDERS)}"
        )
        sys.exit(1)
    _, text, src, tgt, prov = sys.argv
    result = translate_text(text, src, tgt, prov)
    print(result)
