"""[LATER-STEP] platform_brief_audio.py - Generate spoken briefings from platform outputs"""

import os
from model_client import get_managed_model_client
from model_models import PlatformInvocationResult
from tts import text_to_speech  # hypothetical TTS wrapper using the concrete provider


def generate_briefing(
    invocation_result: PlatformInvocationResult, locale: str = "en-US"
) -> bytes:
    """
    Create a short spoken briefing from the model output using Azure AI Speech TTS.

    Args:
        invocation_result: Primary model response.
        locale: Language / locale for the synthesized speech.
    Returns:
        Raw audio bytes (e.g., PCM) ready for playback or storage.
    """
    text = (
        invocation_result.data
        if isinstance(invocation_result.data, str)
        else str(invocation_result.data)
    )
    # Use provider‑specific TTS client (Azure Speech SDK in this example)
    audio_bytes = text_to_speech(text, locale=locale)  # concrete SDK returns bytes
    return audio_bytes
