import requests


def transcribe_audio(audio_bytes: bytes, language: str = 'en-US') -> str:
    url = 'https://api.assemblyai.com/v2/transcript'
    key = __import__('os').getenv('ASSEMBLYAI_API_KEY', '')
    response = requests.post(url, headers={'authorization': key}, json={'audio_data': audio_bytes.decode('latin1'), 'language_code': language}, timeout=60)
    response.raise_for_status()
    return response.json().get('text', '')
