from typing import List, Optional

from speech_client import get_tts_client
from speech_models import Voice

def list_available_voices(language_code: str = "en-US") -> List[Voice]:
    """
    Lists available voices for a given language from Google Cloud Text-to-Speech.

    Args:
        language_code: The IETF language tag (e.g., "en-US", "fr-FR").

    Returns:
        A list of Voice objects matching the language code.
    """
    client = get_tts_client()
    response = client.list_voices(language_code=language_code)
    
    voices = []
    for voice in response.voices:
        voices.append(
            Voice(
                name=voice.name,
                language_codes=list(voice.language_codes),
                ssml_gender=voice.ssml_gender.name,
            )
        )
    return voices

def find_voice(language_code: str, name_substring: Optional[str] = None) -> Optional[Voice]:
    """Finds a specific voice by language and name."""
    voices = list_available_voices(language_code)
    if not name_substring:
        return voices[0] if voices else None

    for voice in voices:
        if name_substring.lower() in voice.name.lower():
            return voice
    return None
