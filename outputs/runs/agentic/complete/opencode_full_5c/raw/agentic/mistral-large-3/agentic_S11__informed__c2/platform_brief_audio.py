from typing import Dict, Any, Optional
import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import io


def platform_brief_audio(
    text: str, voice: Optional[str] = "en-US_AllisonV3Voice"
) -> Dict[str, Any]:
    """
    Generates spoken briefings from text using IBM Watson Text to Speech.
    """
    api_key = os.getenv("IBM_TTS_APIKEY")
    service_url = os.getenv("IBM_TTS_URL")

    if not api_key or not service_url:
        raise ValueError(
            "IBM_TTS_APIKEY and IBM_TTS_URL environment variables must be set"
        )

    try:
        authenticator = IAMAuthenticator(api_key)
        text_to_speech = TextToSpeechV1(authenticator=authenticator)
        text_to_speech.set_service_url(service_url)

        audio_file = io.BytesIO()
        response = text_to_speech.synthesize(
            text, voice=voice, accept="audio/wav"
        ).get_result()

        audio_file.write(response.content)
        audio_file.seek(0)

        return {
            "provider": "ibm_watson",
            "audio_content": audio_file.read(),
            "audio_format": "wav",
            "voice": voice,
        }
    except Exception as e:
        raise RuntimeError(f"IBM Watson Text to Speech failed: {str(e)}")
