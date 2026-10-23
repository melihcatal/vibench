from __future__ import annotations

import os
import sys

from translation_client import load_auth_token, normalize_request, get_provider_config
from translation_models import BatchTranslateRequest, BatchTranslateResponse

# Map of provider name to entrypoint function (stubbed here)
PROVIDERS = {
    "deepl": "batch_translate_deepl",
    "google": "batch_translate_google",
    "azure": "batch_translate_azure",
    "amazon": "batch_translate_amazon",
    "alibaba": "batch_translate_alibaba",
}


def batch_translate(
    texts: list[str],
    source_lang: str,
    target_lang: str,
    provider: str = "deepl",
) -> BatchTranslateResponse:
    """
    Translate a list of strings while preserving input order.

    Args:
        texts: List of source texts.
        source_lang: ISO 639-1 source language code.
        target_lang: ISO 639-1 target language code.
        provider: Provider identifier (default 'deepl').

    Returns:
        BatchTranslateResponse dict containing ordered translated_texts.
    """
    if provider not in PROVIDERS:
        raise ValueError(
            f"Unsupported provider: {provider}. Choose from {list(PROVIDERS)}"
        )

    auth_token = load_auth_token(provider)
    cfg = get_provider_config(provider)
    # Normalizing a list of texts; each SDK will expect a collection field
    payload = normalize_request(
        {"texts": texts, "source_lang": source_lang, "target_lang": target_lang},
        provider,
    )
    # Call the concrete provider function (stubs below)
    result = globals()[PROVIDERS[provider]](auth_token, payload)
    return result


# --------------------------------------------------------------------
# Concrete provider stubs (replace with real SDK calls in production)
# --------------------------------------------------------------------
def batch_translate_deepl(auth: str, payload: dict) -> BatchTranslateResponse:
    """Stub for DeepL batch call."""
    # from deep import translate_batch
    # results = deepl_batch.translate_text_list(payload['texts'], source_lang=payload['source_lang'], target_lang=payload['target_lang'])
    return BatchTranslateResponse(
        translated_texts=[
            f"[DeePL] '{t}' → {payload['target_lang']}" for t in payload["texts"]
        ],
        sources=[payload["source_lang"]] * len(payload["texts"]),
        targets=[payload["target_lang"]] * len(payload["texts"]),
    )


def batch_translate_google(auth: str, payload: dict) -> BatchTranslateResponse:
    """Stub for Google Cloud batch call."""
    # from google.cloud import translate_v2 as translate
    # client = translate.Client(credentials=auth)
    # results = client.translate(texts=payload['texts'], source_language=payload['source_lang'], target_language=payload['target_lang'])
    return BatchTranslateResponse(
        translated_texts=[
            f"[Google] '{t}' → {payload['target_lang']}" for t in payload["texts"]
        ],
        sources=[payload["source_lang"]] * len(payload["texts"]),
        targets=[payload["target_lang"]] * len(payload["texts"]),
    )


def batch_translate_azure(auth: str, payload: dict) -> BatchTranslateResponse:
    """Stub for Azure AI Translator batch call."""
    # from azure.ai.translation.text import TextTranslationClient
    # client = TextTranslationClient(endpoint=\"https://<region>.translator.azure.net\", credential=auth)
    # results = client.translate(texts=payload['texts'], source_language=payload['source_lang'], target_language=payload['target_lang'])
    return BatchTranslateResponse(
        translated_texts=[
            f"[Azure] '{t}' → {payload['target_lang']}" for t in payload["texts"]
        ],
        sources=[payload["source_lang"]] * len(payload["texts"]),
        targets=[payload["target_lang"]] * len(payload["texts"]),
    )


def batch_translate_amazon(auth: str, payload: dict) -> BatchTranslateResponse:
    """Stub for Amazon Translate batch call."""
    # import boto3
    # client = boto3.client('translate', region_name=..., aws_access_key_id=..., aws_secret_access_key=...)
    # results = client.TranslateText(Text=payload['texts'], SourceLanguageCode=payload['source_lang'], TargetLanguageCode=payload['target_lang'])
    return BatchTranslateResponse(
        translated_texts=[
            f"[Amazon] '{t}' → {payload['target_lang']}" for t in payload["texts"]
        ],
        sources=[payload["source_lang"]] * len(payload["texts"]),
        targets=[payload["target_lang"]] * len(payload["texts"]),
    )


def batch_translate_alibaba(auth: str, payload: dict) -> BatchTranslateResponse:
    """Stub for Alibaba batch call."""
    # from aliyun.openapi import client as AcsClient
    # results = client.get_response('TranslateBatch', payload)
    return BatchTranslateResponse(
        translated_texts=[
            f"[Alibaba] '{t}' → {payload['target_lang']}" for t in payload["texts"]
        ],
        sources=[payload["source_lang"]] * len(payload["texts"]),
        targets=[payload["target_lang"]] * len(payload["texts"]),
    )


# --------------------------------------------------------------------
# CLI helper for quick testing
# --------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print(
            f'Usage: {sys.argv[0]} "text1,text2,..." <source_lang> <target_lang> <provider>\nProvider choices: {", ".join(PROVIDERS)}'
        )
        sys.exit(1)
    _, raw_texts, src, tgt, prov = sys.argv
    texts = [t.strip() for t in raw_texts.split(",") if t.strip()]
    result = batch_translate(texts, src, tgt, prov)
    print(result)
