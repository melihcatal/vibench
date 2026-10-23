import requests

from speech_client import get_config, headers
from speech_models import normalize_transcript


def poll_transcription(transcript_id):
    cfg = get_config()
    r = requests.get(
        f"{cfg['assemblyai_base_url']}/transcript/{transcript_id}",
        headers=headers(),
        timeout=60,
    )
    r.raise_for_status()
    return normalize_transcript(r.json())
