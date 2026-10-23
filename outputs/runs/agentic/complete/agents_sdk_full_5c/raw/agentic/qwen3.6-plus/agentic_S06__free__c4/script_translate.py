"""
script_translate.py - Translate narration scripts before synthesis.

Uses the Azure Translator Text API (Cognitive Services) to translate
narration scripts between languages before feeding them to TTS synthesis.
Provider: Microsoft Azure Cognitive Services Translator Text API
Endpoint: https://api.cognitive.microsofttranslator.com/translate
"""

import os
import requests
from typing import Optional, List, Dict

from speech_models import TTSRequest


# Azure Translator endpoint
AZURE_TRANSLATOR_ENDPOINT = os.environ.get(
    "AZURE_TRANSLATOR_ENDPOINT",
    "https://api.cognitive.microsofttranslator.com/translate",
)
AZURE_TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY", "")
AZURE_TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION", "global")


def translate_script(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    subscription_key: Optional[str] = None,
    region: Optional[str] = None,
) -> str:
    """
    Translate a narration script using Azure Cognitive Services Translator.

    Sends text to the Azure Translator Text API for neural machine translation
    before TTS synthesis. Uses the v3 translation endpoint.

    Args:
        text: Source narration script text.
        target_language: Target language code (e.g., 'fr', 'de', 'ja').
        source_language: Optional source language code. Auto-detected if None.
        subscription_key: Azure Translator subscription key.
        region: Azure Translator region.

    Returns:
        Translated text string.
    """
    key = subscription_key or AZURE_TRANSLATOR_KEY
    region = region or AZURE_TRANSLATOR_REGION
    endpoint = AZURE_TRANSLATOR_ENDPOINT

    if not key:
        raise ValueError("Azure Translator subscription key is required.")

    params = {
        "api-version": "3.0",
        "to": target_language,
    }
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    body = [{"text": text}]

    try:
        response = requests.post(
            endpoint,
            params=params,
            headers=headers,
            json=body,
            timeout=30,
        )
        response.raise_for_status()

        result = response.json()
        translated = result[0]["translations"][0]["text"]
        return translated

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Azure Translator API error: {exc}") from exc


def translate_script_batch(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
    subscription_key: Optional[str] = None,
    region: Optional[str] = None,
) -> List[str]:
    """
    Translate multiple narration scripts in a single Azure Translator API call.

    Batches up to 100 texts into one request to the Azure Translator service.

    Args:
        texts: List of source narration script texts.
        target_language: Target language code.
        source_language: Optional source language code.
        subscription_key: Azure Translator subscription key.
        region: Azure Translator region.

    Returns:
        List of translated text strings.
    """
    key = subscription_key or AZURE_TRANSLATOR_KEY
    region = region or AZURE_TRANSLATOR_REGION
    endpoint = AZURE_TRANSLATOR_ENDPOINT

    if not key:
        raise ValueError("Azure Translator subscription key is required.")

    params = {"api-version": "3.0", "to": target_language}
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    body = [{"text": t} for t in texts]

    try:
        response = requests.post(
            endpoint,
            params=params,
            headers=headers,
            json=body,
            timeout=30,
        )
        response.raise_for_status()

        result = response.json()
        return [item["translations"][0]["text"] for item in result]

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Azure Translator API error: {exc}") from exc


def prepare_tts_request_for_translation(
    request: TTSRequest,
    target_language: str,
    subscription_key: Optional[str] = None,
    region: Optional[str] = None,
) -> TTSRequest:
    """
    Translate a TTS request text and return a new request with translated text.

    Uses Azure Translator to translate the text, then maps the target
    language code to the appropriate Azure TTS locale and voice.

    Args:
        request: Original TTSRequest.
        target_language: Target language code (e.g., 'fr' -> 'fr-FR').
        subscription_key: Azure Translator subscription key.
        region: Azure Translator region.

    Returns:
        New TTSRequest with translated text and updated locale.
    """
    language_to_locale = {
        "fr": "fr-FR",
        "de": "de-DE",
        "es": "es-ES",
        "ja": "ja-JP",
        "zh": "zh-CN",
        "pt": "pt-BR",
        "en": "en-US",
    }

    translated_text = translate_script(
        text=request.text,
        target_language=target_language,
        subscription_key=subscription_key,
        region=region,
    )

    new_locale = language_to_locale.get(target_language, f"{target_language}-{target_language.upper()}")
    new_voice = f"{new_locale}-Neural"

    return TTSRequest(
        text=translated_text,
        voice_name=new_voice,
        locale=new_locale,
        output_format=request.output_format,
    )
