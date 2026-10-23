from typing import List, Optional
from speech_client import get_tts_client
from speech_models import Voice

def list_voices(language_code: str) -> List[Voice]:
    """
    Lists available text-to-speech voices for a given language.

    Args:
        language_code: The IETF language tag (e.g., "en-US").

    Returns:
        A list of Voice models.
    """
    client = get_tts_client()
    response = client.list_voices(language_code=language_code)
    
    voices = [Voice.from_google_voice(voice) for voice in response.voices]
    return voices

def find_voice(language_code: str, preferred_name: Optional[str] = None) -> Optional[Voice]:
    """
    Finds a specific voice or a default for the language.

    Args:
        language_code: The language to search for.
        preferred_name: A specific voice name to find.

    Returns:
        A single Voice model or None if not found.
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
