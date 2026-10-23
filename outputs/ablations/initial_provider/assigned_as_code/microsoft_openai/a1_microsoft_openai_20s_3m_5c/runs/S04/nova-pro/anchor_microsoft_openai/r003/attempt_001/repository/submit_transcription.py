import os
import requests


def submit_transcription(payload, config=None):
    config = config or {}
    response = requests.post(
        f"https://{config['region']}.api.cognitive.microsoft.com/speechtotext/transcriptions:submit",
        params={'api-version': '2024-11-15'},
        headers={'Ocp-Apim-Subscription-Key': config.get('api_key') or os.environ['AZURE_SPEECH_KEY']},
        json={'displayName': config.get('job_name', 'transcription'),
              'locale': payload['language_code'], 'contentUrls': [payload['audio_uri']]}, timeout=30)
    response.raise_for_status()
    return {'job_id': response.json()['self'], 'status': 'SUBMITTED'}
