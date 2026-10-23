import json
import urllib.request

from speech_client import get_base_url, get_headers
from speech_models import build_transcription_request, normalize_transcript_payload


def submit_transcription(audio_url, **kwargs):
    data = json.dumps(build_transcription_request(audio_url, **kwargs)).encode("utf-8")
    req = urllib.request.Request(
        f"{get_base_url()}/transcript", data=data, headers=get_headers(), method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return normalize_transcript_payload(json.loads(resp.read().decode("utf-8")))
