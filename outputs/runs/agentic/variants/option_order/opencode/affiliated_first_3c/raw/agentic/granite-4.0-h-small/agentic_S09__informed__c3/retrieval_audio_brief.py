import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def generate_audio_brief(text: str) -> bytes:
    """Generate a spoken audio brief from retrieved search results using IBM Text to Speech.

    Returns the raw audio bytes (WAV format).
    """
    api_key = os.getenv("IBM_TTS_APIKEY")
    service_url = os.getenv("IBM_TTS_URL")
    if not api_key or not service_url:
        raise RuntimeError("Set IBM_TTS_APIKEY and IBM_TTS_URL environment variables")

    authenticator = IAMAuthenticator(api_key)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(service_url)

    response = tts.synthesize(
        text=text, accept="audio/wav", voice="en-US_MichaelV3Voice"
    ).get_result()
    return response.content
