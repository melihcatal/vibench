import requests
from speech_client import load_config, speech_base_url, auth_headers


def request_diarized_transcript(payload, config=None):
    config = load_config(config)
    url = f"{speech_base_url(config['region'])}/transcriptions"
    body = {
        'displayName': config['job_name'],
        'locale': payload['language_code'],
        'contentUrls': [payload['audio_uri']],
        'properties': {'diarizationEnabled': True, 'wordLevelTimestampsEnabled': True},
    }
    response = requests.post(url, headers=auth_headers(config), json=body, timeout=30)
    response.raise_for_status()
    return {'job_id': response.json()['self'], 'status': 'SUBMITTED'}
