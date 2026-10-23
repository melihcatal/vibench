import json
import time
import urllib.request

from speech_client import get_base_url, get_headers
from speech_models import normalize_transcript_payload


def poll_transcription(transcript_id, interval_seconds=5, timeout_seconds=900):
    deadline = time.time() + timeout_seconds
    while True:
        req = urllib.request.Request(
            f"{get_base_url()}/transcript/{transcript_id}",
            headers=get_headers(),
            method="GET",
        )
        with urllib.request.urlopen(req) as resp:
            payload = normalize_transcript_payload(
                json.loads(resp.read().decode("utf-8"))
            )
        if payload.get("status") == "completed":
            return payload
        if payload.get("status") == "error":
            return payload
        if time.time() >= deadline:
            return payload
        time.sleep(interval_seconds)
