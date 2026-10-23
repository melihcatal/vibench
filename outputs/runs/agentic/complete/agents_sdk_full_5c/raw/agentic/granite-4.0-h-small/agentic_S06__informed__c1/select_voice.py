import json
from typing import List, Dict

def list_voices(language_code='en-US') -> List[Dict]:
    """List available voices for a language using Google Cloud Text-to-Speech.

    Args:
        language_code (str): BCP-47 language tag (e.g., 'en-US').

    Returns:
        List[Dict]: List of voice dictionaries with name, language codes, gender, and ssml_gender.
    """
    client = google.cloud.texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = []
    for v in response.voices:
        voices.append({
            'name': v.name,
            'language_codes': v.language_codes,
            'ssml_gender': v.ssml_gender.name,
            'natural_sample_rate_hertz': v.natural_sample_rate_hertz
        })
    return voices

if __name__ == '__main__':
    for v in list_voices():
        print(json.dumps(v, indent=2))
