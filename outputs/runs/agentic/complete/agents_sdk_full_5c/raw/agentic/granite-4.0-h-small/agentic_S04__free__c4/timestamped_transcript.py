import os
import time
from speech_client import SpeechClient

# Provider-specific: Azure Speech Services batch transcription with timestamps
AZURE_SPEECH_ENDPOINT = os.getenv('AZURE_SPEECH_ENDPOINT')
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')

client = SpeechClient(
    base_url=AZURE_SPEECH_ENDPOINT,
    api_key=AZURE_SPEECH_KEY,
    provider='azure_speech'
)

def timestamped_transcript(job_id: str, format: str = 'json') -> dict:
    """Retrieve a transcription result with word/segment timestamps.

    Args:
        job_id (str): Transcription job identifier.
        format (str): Output format ('json' or 'txt').
    Returns:
        dict: JSON payload containing timestamps for each word/segment.
    """
    endpoint = f'/batch/transcriptions/{job_id}/timings'
    response = client.get(endpoint, params={'format': format})
    return response.json()

if __name__ == '__main__':
    # Example usage (replace with real job ID)
    job_id = 'job-2025-08-15-001'
    result = timestamped_transcript(job_id)
    print('Timestamped transcript:', result)
