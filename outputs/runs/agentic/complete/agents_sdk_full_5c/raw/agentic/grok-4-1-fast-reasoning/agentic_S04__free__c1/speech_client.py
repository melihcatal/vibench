import os
from assemblyai import Client

def get_speech_client() -> Client:
    api_key = os.getenv('ASSEMBLYAI_API_KEY')
    if not api_key:
        raise ValueError('ASSEMBLYAI_API_KEY environment variable is required.')
    return Client(api_key=api_key)