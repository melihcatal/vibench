import os
import json
from speech_client import SpeechClient
from speech_models import TranscriptRequest

# Provider-specific: Azure Speech Services batch transcription with speaker diarization
AZURE_SPEECH_ENDPOINT = os.getenv('AZURE_SPEECH_ENDPOINT')
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')

client = SpeechClient(
    base_url=AZURE_SPEECH_ENDPOINT,
    api_key=AZURE_SPEECH_KEY,
    provider='azure_speech'
)

def diarized_transcript(audio_blob_id: str, speaker_count: int = 2, language: str = 'en-US'):
    """Request batch transcription with speaker diarization.

    Args:
        audio_blob_id (str): Audio file identifier stored in the cloud.
        speaker_count (int): Number of speakers to separate.
        language (str): Language code for transcription.
    Returns:
        dict: Job details containing diarized transcription metadata.
    """
    payload = {
        "contentUrls": [audio_blob_id],
        "properties": {
            "language": language,
            "diarization": {
                "speakerCount": speaker_count
            }
        }
    }
    response = client.post('/batch/transcriptions', json=payload)
    return response.json()

if __name__ == '__main__':
    # Example usage
    job = diarized_transcript(audio_blob_id='https://mystorage.blob/core/meeting.wav', speaker_count=3)
    print('Diarized job submitted:', job)
