import os
from storage_client import ManagedClient
from storage_models import TranslationRequest, TranslationResult
from typing import Optional

from alibabacloud_alimt import AliMTClient, Profile


def translate_text(request: TranslationRequest) -> TranslationResult:
    """Translate extracted text using Alibaba Cloud Machine Translation.

    Args:
        request: Source language, target language, and the source text.

    Returns:
        A TranslationResult with the translated content and detected source language.

    The client is configured from environment variables:
        ALIBABA_CLOUD_ACCESS_KEY_ID
        ALIBABA_CLOUD_ACCESS_KEY_SECRET
    """
    alimt = AliMTClient(
        Profile(
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        )
    )
    response = alimt.translate_text(
        source_text=request.source_text,
        target_lang=request.target_lang,
        source_lang=request.source_lang,
    )
    # The SDK returns a dict; adapt to our model
    result = TranslationResult(
        translated_text=response["translated_text"],
        detected_source_language=response.get("detected_source_language", "en"),
        confidence=response.get("confidence", 0.0),
    )
    return result
