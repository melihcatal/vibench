# SAME-SCENARIO: select_voice.py
# List available voices for a locale and optionally select one using IBM Watson TTS

import os
import ibm_watson
from ibm_watson import TextToSpeechV1

# Load credentials from environment variables (ensure they are set before running)
IBM_TTS_APIKEY = os.getenv('IBM_TTS_APIKEY')
IBM_TTS_URL = os.getenv('IBM_TTS_URL')

# Initialize client using SDK
tts_client = TextToSpeechV1(authenticator=ibm_watson.IamAuthenticator(IBM_TTS_APIKEY))
tts_client.set_service_url(IBM_TTS_URL)

def list_voices(locale: str = 'en-US') -> list:
    """List all voices available for a given locale.

    Args:
        locale: Locale string (e.g., 'en-US', 'es-ES').

    Returns:
        List of voice dictionaries containing name and gender.
    """
    response = tts_client.list_voices(locale=locale).get_result()
    return response.get('voices', [])


def select_voice(locale: str = 'en-US') -> str:
    """Prompt user to select a voice for the locale (for demo purposes).

    Args:
        locale: Locale string (e.g., 'en-US').

    Returns:
        Selected voice name.
    """
    voices = list_voices(locale)
    print('Available voices for', locale, ':")
    for i, voice in enumerate(voices, 1):
        print(f'  {i}. {voice.name} ({voice.gender})')
    choice = int(input('Select a voice number: '))
    return voices[choice - 1].name

# Example usage
if __name__ == '__main__':
    selected = select_voice('en-US')
    print('Selected voice:', selected)
