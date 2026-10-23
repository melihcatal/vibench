from typing import List, Dict, Optional
from speech_client import get_tts_client

def list_voices(locale: str = 'en-US') -> List[Dict[str, str]]:
    """
    Lists available voices for a target locale using Google Cloud TTS.
    """
    client = get_tts_client()
    response = client.list_voices(language_code=locale)
    voices = []
    for voice in response.voices:
        voice_info = {
            'name': voice.name,
            'language_codes': ','.join(voice.language_codes),
            'ssml_gender': voice.ssml_gender.name if voice.ssml_gender else 'NEUTRAL',
            'natural_sample_rate_hertz': str(voice.natural_sample_rate_hertz)
        }
        voices.append(voice_info)
    return voices

def select_voice(locale: str = 'en-US', preferred_gender: Optional[str] = None, neural: bool = True) -> str:
    """
    Selects a suitable voice for the target locale.
    Prefers neural voices.
    """
    voices = list_voices(locale)
    candidates = []
    for v in voices:
        is_neural = any(x in v['name'] for x in ['Neural2', 'Wavenet', 'Neural'])
        if neural and not is_neural:
            continue
        if preferred_gender and preferred_gender.upper() not in v['ssml_gender']:
            continue
        candidates.append(v['name'])
    return candidates[0] if candidates else voices[0]['name']
