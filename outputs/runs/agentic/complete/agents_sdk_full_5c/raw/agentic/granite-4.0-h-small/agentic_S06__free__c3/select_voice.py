# select_voice.py
# [SAME-SCENARIO]
# Helper to list available voices for a locale or select a specific voice.

from google.cloud import texttospeech

# Helper utilities from same-scenario local files
from speech_client import TextToSpeechClient

def list_voices(language_code: str = "en-US"):
    """List all voices available for a given language code.
    Args:
        language_code: BCP-47 language identifier (default en-US).
    Returns:
        List of (voice_name, language_codes, gender, sample_rate_hertz) tuples.
    """
    client = TextToSpeechClient()
    voices = client.list_voices(language_code=language_code)
    return [(v.name, v.language_codes, v.ssml_gender, v.natural_sample_rate_hertz) for v in voices.voices]

def select_voice(language_code: str = "en-US") -> str:
    """Select a default voice name for a target locale.
    Args:
        language_code: BCP-47 language identifier (default en-US).
    Returns:
        A suitable voice name (e.g., 'en-US-Wavenet-A').
    """
    voices = list_voices(language_code)
    # Simple heuristic: pick the first Wavenet voice if available, else standard
    for v in voices:
        if 'Wavenet' in v[0]:
            return v[0]
    return voices[0][0]
