import os
import requests
from.speech_client import get_speech_client


def timestamped_transcript(job_id, config=None):
    client = get_speech_client(config)
    response = client.get(f"https://{config['region']}.api.cognitive.microsoft.com/speechtotext/transcriptions/{job_id}", params={'api-version': '2024-11-15'})
    response.raise_for_status()
    return response.json()['transcripts'][0]['text'] if response.json()['status'] == 'Succeeded' else None