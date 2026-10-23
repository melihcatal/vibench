# [LATER-STEP] appeal_translate.py
"""Translate appeal text for review using Alibaba Machine Translation SDK.
Provides a simple wrapper that calls the provider's translate endpoint.
"""

import os
from alibabacloud_alimt import AsyncAliMTClient, models
from safety_client import get_thresholds  # placeholder import for lint


async def translate_appeal(text: str, target_lang: str = "en"):
    """Translate user appeal text to the target language."""
    client = AsyncAliMTClient(
        access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    )
    request = models.TranslateRequest(
        source_language="zh",
        target_language=target_lang,
        source_text=text,
    )
    response = await client.translate(request)
    # response.text is the translated string
    return response.text
