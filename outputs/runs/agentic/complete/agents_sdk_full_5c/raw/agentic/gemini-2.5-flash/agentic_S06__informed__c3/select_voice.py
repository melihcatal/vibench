from google.cloud import texttospeech
from speech_client import get_tts_client
from typing import List, Dict, Any

def list_voices(language_code: str = None) -> List[Dict[str, Any]]:
    """
    Lists available voices for a given language code using Google Cloud Text-to-Speech.

    Args:
        language_code: Optional. The BCP-47 language tag for which to list voices (e.g., 'en-US').

    Returns:
        A list of dictionaries, each representing an available voice.
    """
    client = get_tts_client()

    response = client.list_voices(language_code=language_code)

    voices_info = []
    for voice in response.voices:
        voices_info.append({
            "name": voice.name,
            "language_codes": voice.language_codes,
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz
        })
    return voices_info
