import json
import urllib.request

from speech_client import auth_headers, openai_base_url
from speech_models import normalize_transcript_text


def poll_transcription(job_id: str) -> str:
    req = urllib.request.Request(
        f"{openai_base_url()}/responses/{job_id}",
        headers=auth_headers(),
        method="GET",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return normalize_transcript_text(data)
