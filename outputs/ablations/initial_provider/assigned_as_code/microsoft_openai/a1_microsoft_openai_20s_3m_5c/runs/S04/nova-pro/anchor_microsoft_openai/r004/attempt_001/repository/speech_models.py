def create_transcription_request(payload, job_name='transcription'):
    return {
        'displayName': job_name,
        'locale': payload['language_code'],
        'contentUrls': [payload['audio_uri']]
    }


def normalize_transcription_response(response):
    return {
        'job_id': response['self'],
        'status': 'SUBMITTED'
    }