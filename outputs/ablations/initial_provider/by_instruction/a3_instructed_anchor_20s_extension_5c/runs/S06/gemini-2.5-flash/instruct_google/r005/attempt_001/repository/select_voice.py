from google.cloud import texttospeech
from typing import List, Dict, Any

def list_voices(language_code: str = None) -> List[Dict[str, Any]]:
    """Lists available voices for a given language code using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code).voices

    voice_details = []
    for voice in voices:
        voice_details.append({
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        })
    return voice_details

def select_voice(language_code: str, ssml_gender: texttospeech.SsmlVoiceGender) -> texttospeech.VoiceSelectionParams:
    """Selects a voice based on language code and SSML gender."""
    return texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=ssml_gender
    )
