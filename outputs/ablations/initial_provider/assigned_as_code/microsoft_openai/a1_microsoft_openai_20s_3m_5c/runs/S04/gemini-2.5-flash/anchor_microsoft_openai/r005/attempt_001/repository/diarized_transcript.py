import os
import requests


def diarized_transcript(payload, config=None):
    config = config or {}
    # Azure Speech-to-Text handles diarization as part of the transcription request.
    # We will simulate submitting a new transcription request with diarization enabled.
    # In a real scenario, the submit_transcription function would be enhanced
    # to include diarization settings. For this exercise, we'll assume a new submission.
    response = requests.post(
        f"https://{config['region']}.api.cognitive.microsoft.com/speechtotext/transcriptions:submit",
        params={'api-version': '2024-11-15'},
        headers={'Ocp-Apim-Subscription-Key': config.get('api_key') or os.environ['AZURE_SPEECH_KEY']},
        json={
            'displayName': config.get('job_name', 'diarized_transcription'),
            'locale': payload['language_code'],
            'contentUrls': [payload['audio_uri']],
            'properties': {
                'diarizationEnabled': True,
                'wordLevelTimestampsEnabled': True  # Often enabled with diarization
            }
        },
        timeout=30)
    response.raise_for_status()
    return {'job_id': response.json()['self'], 'status': 'SUBMITTED_FOR_DIARIZATION'}
