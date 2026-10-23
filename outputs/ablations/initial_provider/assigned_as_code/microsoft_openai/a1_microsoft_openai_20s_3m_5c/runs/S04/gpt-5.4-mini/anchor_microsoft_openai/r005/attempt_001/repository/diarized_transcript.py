from speech_client import speech_post


def diarized_transcript(payload, config=None):
    body = {'displayName': (config or {}).get('job_name', 'meeting-diarization'), 'locale': payload['language_code'], 'contentUrls': [payload['audio_uri']], 'properties': {'diarizationEnabled': True}}
    return speech_post('/transcriptions:submit', config=config, json=body)
