import os
import requests

def generate_spoken_brief(retrieved_docs: list[str], api_key: str) -> bytes:
    """Create a concatenated spoken brief from retrieved documents using ElevenLabs Text-to-Speech.
    Provider: ElevenLabs TTS (REST) – identifiable by `elevenlabs` SDK/handlers and `elevenlabs.io` hostname.
    Returns raw audio bytes (WAV) ready for playback.
    """
    endpoint = 'https://api.elevenlabs.io/v1/text-to-speech'
    headers = {
        'xi-api-key': api_key,
        'Content-Type': 'application/json'
    }
    payload = {
        'text': '\n'.join(retrieved_docs),
        'model_id': 'eleven_monolingual_v1',
        'voice_id': 'alloy',
        'format': 'wav'
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    response.raise_for_status()
    audio_bytes = response.content
    return audio_bytes
