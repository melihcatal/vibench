import json
import urllib.request

from speech_client import get_base_url, get_headers
from speech_models import build_diarization_request, normalize_transcript_payload


def diarized_transcript(audio_url, **kwargs):
    data = json.dumps(build_diarization_request(audio_url, **kwargs)).encode("utf-8")
    req = urllib.request.Request(
        f"{get_base_url()}/transcript", data=data, headers=get_headers(), method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return normalize_transcript_payload(json.loads(resp.read().decode("utf-8")))
