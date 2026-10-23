# later-step implementation - translate narration scripts before synthesis

from __future__ import annotations
import json
from typing import Any, Dict
from google.cloud import translate_v2 as translate
from speech_models import SynthesizeRequest
from speech_client import get_azure_client

# Provider: Google Cloud Translation API (explicit import google.cloud.translate_v2)


async def translate_script(source_text: str, target_locale: str = "en-US") -> str:
    """Translate narration script to target locale using Google Translate."""
    client = translate.Client()
    result = client.translate(source_text, target_language=target_locale)
    return result["translatedText"]


async def translate_request(
    request: SynthesizeRequest, target_locale: str
) -> SynthesizeRequest:
    """Create a new request with translated text."""
    translated = await translate_script(request.text, target_locale)
    return SynthesizeRequest(
        text=translated,
        ssml=request.ssml,
        voice_name=request.voice_name,
        locale=target_locale,
    )
