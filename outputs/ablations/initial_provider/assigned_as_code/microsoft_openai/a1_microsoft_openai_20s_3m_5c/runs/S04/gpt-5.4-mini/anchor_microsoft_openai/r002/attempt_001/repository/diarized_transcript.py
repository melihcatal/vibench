from speech_client import http_post, speech_headers, transcription_url, load_config


def diarized_transcript(payload, config=None):
    config = load_config(config)
    body = {
        'displayName': config['job_name'],
        'locale': payload['language_code'],
        'contentUrls': [payload['audio_uri']],
        'properties': {'diarizationEnabled': True},
    }
    response = http_post(
        transcription_url(config, '/speechtotext/transcriptions:submit'),
        headers=speech_headers(config),
        params={'api-version': '2024-11-15'},
        json=body,
        timeout=30,
    )
    data = response.json()
    return {'job_id': data['self'], 'status': 'SUBMITTED', 'diarization': True}
