from speech_client import get_polly_client
from speech_models import VoiceSelectionInput
from typing import List, Dict, Any

def select_voice(payload: VoiceSelectionInput) -> List[Dict[str, Any]]:
    client = get_polly_client()
    response = client.describe_voices(LanguageCode=payload.language_code, IncludeAdditionalLanguageCodes=True)
    voices = response["Voices"]
    
    filtered_voices = []
    for voice in voices:
        if payload.gender and voice["Gender"] != payload.gender:
            continue
        filtered_voices.append(voice)
    
    return filtered_voices
