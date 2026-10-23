from speech_client import http_get, speech_headers, transcription_url, load_config
from speech_models import extract_words, extract_segments


def timestamped_transcript(job_id, config=None):
    config = load_config(config)
    response = http_get(
        transcription_url(config, f"/speechtotext/transcriptions/{job_id}"),
        headers=speech_headers(config),
        params={'api-version': '2024-11-15'},
        timeout=30,
    )
    data = response.json()
    return {'job_id': job_id, 'segments': extract_segments(data), 'words': extract_words(data)}
