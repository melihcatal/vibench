# [LATER-STEP] platform_brief_audio.py
# Generate spoken briefing from watsonx model output using Watson Text to Speech

import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from typing import Dict


def create_audio_brief(
    output: Dict[str, Any], voice: str = "en-US_MichaelV3Voice"
) -> bytes:
    """Convert generated text to spoken audio using Watson TTS.

    Returns raw audio bytes (WAV format by default).
    """
    api_key = os.getenv("IBM_TTS_APIKEY")
    service_url = os.getenv("IBM_TTS_URL")
    if not api_key or not service_url:
        raise ValueError("Set IBM_TTS_APIKEY and IBM_TTS_URL environment variables")

    authenticator = IAMAuthenticator(api_key)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(service_url)

    response = tts.synthesize(
        text=output["generated_text"], accept="audio/wav", voice=voice
    )
    return response.get_result().content
