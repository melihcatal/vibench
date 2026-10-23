from typing import List, Optional
from speech_client import get_speech_client
from speech_models import SpeechVoice

def list_voices(language_code: str) -> List[SpeechVoice]:
    """
    Lists available voices for a specific language using Google Cloud Text-to-Speech.

    Args:
        language_code: The BCP-47 language code (e.g., 'en-US', 'fr-FR').

    Returns:
        A list of SpeechVoice objects.
    """
    client = get_speech_client()
    response = client.list_voices(language_code=language_code)
    
    return [SpeechVoice.from_api_voice(voice) for voice in response.voices]

def select_voice(language_code: str, preferred_name: Optional[str] = None) -> Optional[SpeechVoice]:
    """
    Selects a specific voice for a target locale, optionally by name.

    Args:
        language_code: The language code to search for.
        preferred_name: The preferred voice name (e.g., 'en-US-Wavenet-D').

    Returns:
        A SpeechVoice object if a suitable voice is found, otherwise None.
    """
    voices = list_voices(language_code)
    if not voices:
        return None

    if preferred_name:
        for voice in voices:
            if voice.name == preferred_name:
                return voice
    
    # Return the first available voice as a default
    return voices[0] if voices else None
