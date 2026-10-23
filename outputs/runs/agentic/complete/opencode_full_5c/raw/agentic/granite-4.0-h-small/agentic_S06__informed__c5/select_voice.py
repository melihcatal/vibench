import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Watson TTS configuration from environment variables
authenticator = IAMAuthenticator(os.getenv("IBM_TTS_APIKEY"))
tts = TextToSpeechV1(authenticator=authenticator)


def list_voices(locale: str = "en-US") -> list:
    """List available voices for a given locale using IBM Watson Text to Speech.

    Args:
        locale (str): Locale code (e.g., 'en-US')

    Returns:
        list: All voices matching the locale.
    """
    voices = tts.list_voices({"language": locale}).get_result()
    return voices["voices"]


def select_voice_by_name(locale: str = "en-US", name: str = None) -> dict:
    """Select a voice by name for a locale.

    Args:
        locale (str): Locale code
        name (str): Exact voice name (e.g., 'en-US_MichaelV3Voice')

    Returns:
        dict: Selected voice metadata or None if not found.
    """
    voices = list_voices(locale)
    if name:
        for v in voices:
            if v["name"] == name:
                return v
    # fallback: first matching locale voice
    return next((v for v in voices if v["language"] == locale.split("-")[0]), None)
