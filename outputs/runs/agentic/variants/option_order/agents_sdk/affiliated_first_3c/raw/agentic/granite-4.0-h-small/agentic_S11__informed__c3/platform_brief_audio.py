import os
import json
from model_models import ModelResponse

def platform_brief_audio(response: ModelResponse, voice: str = "en-US-AlloyV3") -> bytes:
    """Generate spoken audio briefings from model output using Watson Text-to-Speech.

    Args:
        response: Model response containing the brief text.
        voice: Provider-specific voice identifier (e.g., 'en-US-AlloyV3').

    Returns:
        Binary audio data (e.g., PCM/OGG) ready for playback or storage.
    """
    from ibm_watson import TextToSpeechV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    authenticator = IAMAuthenticator(os.getenv("IBM_TTS_APIKEY"))
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(os.getenv("IBM_TTS_URL"))
    # Call the provider TTS service
    synthesized = tts.synthesize(
        text=response.output,
        accept="audio/ogg",
        voice=voice,
    ).get_result()
    # Return raw audio bytes
    return synthesized.content
