import os
import json
from speech_client import SpeechClient
from speech_models import TranscriptRequest

# Provider-specific: Azure Speech Services batch transcription
AZURE_SPEECH_ENDPOINT = os.getenv('AZURE_SPEECH_ENDPOINT')
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')

client = SpeechClient(
    base_url=AZURE_SPEECH_ENDPOINT,
    api_key=AZURE_SPEECH_KEY,
    provider='azure_speech'
)

def submit_transcription(audio_blob_id: str, language: str = 'en-US'):
    """Submit a batch transcription job for the given audio file.

    Args:
        audio_blob_id (str): Identifier of the audio blob stored in the cloud.
        language (str): Language code for transcription.
    Returns:
        dict: Response containing job ID and status.
    """
    payload = {
        "contentUrls": [audio_blob_id],
        "properties": {"language": language}
    }
    response = client.post('/batch/transcriptions', json=payload)
    return response.json()

if __name__ == '__main__':
    # Example usage (for local testing only)
    result = submit_transcription(audio_blob_id='https://mystorage.blob/core/audio.wav')
    print('Submitted job:', result)
