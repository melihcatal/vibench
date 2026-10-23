# [LATER-STEP] platform_brief_audio.py
# Generate a spoken briefing from watsonx.ai model output using Watson Text to Speech

import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from model_models import NormalizedResponse
from dataclasses import dataclass


@dataclass
class TTSRequest:
    output_text: str
    voice: str = "en-US_MichaelV3Voice"  # default voice; adjust as needed


def synthesize_briefing(text: str, voice: str = "en-US_MichaelV3Voice") -> bytes:
    """Synthesize speech audio from the model's generated text."""
    api_key = os.getenv("WATSONX_API_KEY")
    service_url = os.getenv(
        "WATSONX_SERVICE_URL"
    )  # e.g., https://us-south.text-to-speech.watson.cloud.ibm.com
    if not api_key or not service_url:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_SERVICE_URL environment variables"
        )

    authenticator = IAMAuthenticator(api_key)
    tts = TextToSpeechV1(url=service_url, authenticator=authenticator)
    tts.set_disable_ssl_verification(True)  # for local testing

    # Call synthesize using SSML or plain text
    synthesis = tts.synthesize(
        text=text,
        accept="audio/wav",
        voice=voice,
    ).get_result()
    # Return raw audio bytes (wav format)
    return synthesis.content
