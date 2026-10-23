from.speech_client import create_client

def create_transcription_request(payload, job_name=None):
    return {
        'displayName': job_name or 'transcription',
        'locale': payload['language_code'],
        'contentUrls': [payload['audio_uri']]
    }

def parse_transcription_response(response):
    return {'job_id': response['self'], 'status': 'SUBMITTED'}