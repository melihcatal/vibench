import os
import requests

def timestamped_transcript(job_id, config=None):
    config = config or {}
    response = requests.get(
        f"https://{config['region']}.api.cognitive.microsoft.com/speechtotext/transcriptions/{job_id}/results",
        params={'api-version': '2024-11-15'},
        headers={'Ocp-Apim-Subscription-Key': config.get('api_key') or os.environ['AZURE_SPEECH_KEY']}
    )
    response.raise_for_status()
    return response.json()['results']