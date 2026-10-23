import requests

from speech_client import assemblyai_headers, get_env
from speech_models import normalize_transcript


def timestamped_transcript(job_id: str = ""):
    base_url = get_env("ASSEMBLYAI_BASE_URL", "https://api.assemblyai.com")
    if not job_id:
        job_id = get_env("TRANSCRIPT_ID")
    response = requests.get(
        f"{base_url}/v2/transcript/{job_id}",
        headers=assemblyai_headers(),
        params={"words": "true", "punctuate": "true"},
        timeout=60,
    )
    response.raise_for_status()
    return normalize_transcript(response.json())
