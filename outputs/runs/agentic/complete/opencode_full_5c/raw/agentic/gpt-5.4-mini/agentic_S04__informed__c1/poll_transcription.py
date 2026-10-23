import time
from speech_client import get_json
from speech_models import normalize_transcript_payload


def poll_transcription(
    transcript_id: str, interval_seconds: int = 5, timeout_seconds: int = 600
) -> str:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        result = normalize_transcript_payload(get_json(f"/transcript/{transcript_id}"))
        if result.status == "completed":
            return result.transcript or ""
        if result.status in {"error", "failed"}:
            raise RuntimeError(result.raw or result.status)
        time.sleep(interval_seconds)
    raise TimeoutError("transcription polling timed out")
