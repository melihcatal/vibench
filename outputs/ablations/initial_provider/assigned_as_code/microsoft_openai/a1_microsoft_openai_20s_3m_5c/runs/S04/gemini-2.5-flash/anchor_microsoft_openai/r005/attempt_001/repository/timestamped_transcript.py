import os
import requests


def timestamped_transcript(job_id, config=None):
    config = config or {}
    response = requests.get(
        job_id,
        headers={'Ocp-Apim-Subscription-Key': config.get('api_key') or os.environ['AZURE_SPEECH_KEY']},
        timeout=30)
    response.raise_for_status()
    result = response.json()
    if result['status'] == 'Succeeded':
        files_response = requests.get(
            result['filesUrl'],
            headers={'Ocp-Apim-Subscription-Key': config.get('api_key') or os.environ['AZURE_SPEECH_KEY']},
            timeout=30)
        files_response.raise_for_status()
        for file in files_response.json()['values']:
            if file['kind'] == 'Transcription':
                transcript_response = requests.get(
                    file['links']['contentUrl'],
                    headers={'Ocp-Apim-Subscription-Key': config.get('api_key') or os.environ['AZURE_SPEECH_KEY']},
                    timeout=30)
                transcript_response.raise_for_status()
                # Azure Speech-to-Text transcription results include word-level timestamps if requested
                return {'status': result['status'], 'timestamped_transcript': transcript_response.json()}
    return {'status': result['status'], 'timestamped_transcript': None}
