import requests
import os

def generate_brief_audio_from_platform_output(
    output_text: str,
    voice_id: str = '21m00Tcm4TlvDq8ikWAM'
) -> bytes:
    api_key = os.getenv('ELEVENLABS_API_KEY')
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
    headers = {
        'Accept': 'audio/mpeg',
        'xi-api-key': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        'text': output_text,
        'model_id': 'eleven_monolingual_v1',
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.75
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.content