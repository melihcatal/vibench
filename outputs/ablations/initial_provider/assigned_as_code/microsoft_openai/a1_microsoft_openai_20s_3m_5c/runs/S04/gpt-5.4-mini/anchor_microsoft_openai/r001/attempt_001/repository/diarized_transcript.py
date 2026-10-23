import requests

from speech_client import load_speech_config, speech_endpoint


def diarized_transcript(payload, config=None):
    cfg = load_speech_config(config)
    response = requests.post(
        speech_endpoint(cfg.region, 'speechtotext/transcriptions:submit'),
        params={'api-version': '2024-11-15'},
        headers={'Ocp-Apim-Subscription-Key': cfg.api_key},
        json={'displayName': payload.get('job_name', 'diarized-transcript'), 'locale': payload['language_code'], 'contentUrls': [payload['audio_uri']], 'properties': {'diarizationEnabled': True}},
        timeout=30,
    )
    response.raise_for_status()
    return {'job_id': response.json()['self'], 'status': 'SUBMITTED'}
