from speech_client import get_polly_client
from typing import List, NamedTuple, Optional

class Voice(NamedTuple):
    id: str
    name: str
    gender: str
    language_code: str # AWS provider-specific field
    language_name: str

def select_voice(language_code: Optional[str] = None, gender: Optional[str] = None) -> List[Voice]:
    """
    Lists or selects voices for a target locale using AWS Polly.
    """
    polly_client = get_polly_client()
    response = polly_client.describe_voices()

    voices = []
    for v in response['Voices']:
        if (language_code is None or v['LanguageCode'] == language_code) and \
           (gender is None or v['Gender'].lower() == gender.lower()):
            voices.append(Voice(
                id=v['Id'],
                name=v['Name'],
                gender=v['Gender'],
                language_code=v['LanguageCode'],
                language_name=v['LanguageName']
            ))
    return voices
