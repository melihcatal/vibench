import os
from speech_client import get_polly_client
from speech_models import Voice
from typing import List

def select_voice_by_locale(language_code: str) -> List[Voice]:
    polly_client = get_polly_client()
    response = polly_client.describe_voices(LanguageCode=language_code)
    voices = []
    for voice_data in response['Voices']:
        voices.append(Voice(
            id=voice_data['Id'],
            name=voice_data['Name'],
            language_code=voice_data['LanguageCode']
        ))
    return voices
