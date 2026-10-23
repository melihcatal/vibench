from typing import List, Optional
from speech_client import get_tts_client
from speech_models import VoiceDetail
from google.cloud import texttospeech

def list_available_voices(language_code: str) -> List[VoiceDetail]:
    """
    Lists available voices for a given language code from Google Cloud TTS.

    Args:
        language_code: The language code to filter by (e.g., 'en-US').

    Returns:
        A list of VoiceDetail objects.
    """
    client = get_tts_client()
    response = client.list_voices(language_code=language_code)
    
    voices = []
    for voice in response.voices:
        gender_name = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        for lang_code in voice.language_codes:
            if lang_code.startswith(language_code):
                 voices.append(
                    VoiceDetail(
                        name=voice.name,
                        language_code=lang_code,
                        ssml_gender=gender_name
                    )
                )
    return voices

def select_voice(language_code: str, preferred_name: Optional[str] = None) -> Optional[VoiceDetail]:
    """
    Selects a specific voice or the first available one for a language.
    """
    available_voices = list_available_voices(language_code)
    if not available_voices:
        return None

    if preferred_name:
        for voice in available_voices:
            if voice.name == preferred_name:
                return voice
    
    return available_voices[0]
