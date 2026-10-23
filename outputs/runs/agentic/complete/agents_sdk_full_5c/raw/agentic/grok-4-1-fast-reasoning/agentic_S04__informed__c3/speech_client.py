import os
import assemblyai as aai

def get_speech_client():
    api_key = os.getenv('ASSEMBLYAI_API_KEY')
    if not api_key:
        raise ValueError('ASSEMBLYAI_API_KEY environment variable is required.')
    return aai.Client(api_key=api_key)