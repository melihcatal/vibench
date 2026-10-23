import requests

from speech_client import load_speech_config, speech_endpoint
from speech_models import normalize_transcript


def timestamped_transcript(payload, config=None):
    cfg = load_speech_config(config)
    response = requests.get(
        speech_endpoint(cfg.region, f'speechtotext/transcriptions/{payload["job_id"]}/files'),
        params={'api-version': '2024-11-15', 'wordLevelTimestampsEnabled': 'true'},
        headers={'Ocp-Apim-Subscription-Key': cfg.api_key},
        timeout=30,
    )
    response.raise_for_status()
    return normalize_transcript(response.json())
