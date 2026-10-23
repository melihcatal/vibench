import os
from speech_client import http_get, speech_headers, transcription_url, load_config
from speech_models import normalize_transcript


def poll_transcription(job_id, config=None):
    config = load_config(config)
    response = http_get(
        job_id if isinstance(job_id, str) and job_id.startswith('http') else transcription_url(config, f"/speechtotext/transcriptions/{job_id}"),
        headers=speech_headers(config) if config.get('api_key') else {'Ocp-Apim-Subscription-Key': os.environ['AZURE_SPEECH_KEY']},
        params={'api-version': '2024-11-15'},
        timeout=30,
    )
    return {'job_id': job_id, 'status': response.json().get('status'), 'transcript': normalize_transcript(response.json())}
