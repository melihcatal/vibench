import requests

from speech_client import get_base_url, get_headers
from speech_models import normalize_segments


def timestamped_transcript(job_id: str):
    response = requests.get(
        f"{get_base_url()}/transcript/{job_id}",
        headers=get_headers(),
        params={"word_boost": "true"},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "provider": "assemblyai",
        "job_id": job_id,
        "status": data.get("status", ""),
        "segments": normalize_segments(data.get("words") or data.get("segments")),
    }
