import json
from typing import TypedDict, List


# ---------- Request models ----------
class DiarizationConfig(TypedDict):
    enable: bool
    speaker_count: int


class SubmitPayload(TypedDict):
    audio: str  # Path or URI to the audio file
    language: str
    diarization: Optional[DiarizationConfig]
    callback_url: Optional[str]
    # Add more fields as needed for the chosen provider


# ---------- Response models ----------
class JobStatus(TypedDict):
    job_id: str
    status: str  # e.g., "queued", "completed"


class Segment(TypedDict):
    start: float
    end: float
    text: str


class TranscriptionResult(TypedDict):
    status: str
    segments: List[Segment]


# ---------- Normalization helpers ----------


def normalize_submit_payload(payload: dict) -> SubmitPayload:
    """Convert arbitrary input to the standardized SubmitPayload shape."""
    return SubmitPayload(
        audio=payload.get("audio"),
        language=payload.get("language", "en-US"),
        diarization=payload.get("diarization"),
        callback_url=payload.get("callback_url"),
    )


def normalize_job_response(raw: dict) -> JobStatus:
    return JobStatus(job_id=raw.get("job_id"), status=raw.get("status"))


def normalize_transcript(raw: dict) -> TranscriptionResult:
    # Ensure timestamps are present; fall back to text-only representation
    segments = [
        {
            "start": seg.get("start", 0.0),
            "end": seg.get("end", 0.0),
            "text": seg.get("text", ""),
        }
        for seg in raw.get("segments", [])
    ]
    return TranscriptionResult(status=raw.get("status"), segments=segments)


# Example stubbed functions that a scored file could call
# (they map to the client methods in speech_client.py)


def submit_batch_job(payload: SubmitPayload) -> dict:
    client = get_client()
    return client.submit_batch_job(payload)


def poll_job(job_id: str, timeout: int = 60) -> dict:
    client = get_client()
    while timeout > 0:
        resp = client.get_job_status(job_id)
        if resp["status"] == "completed":
            return resp
        timeout -= 1
        time.sleep(1)
    raise TimeoutError("Polling exceeded")


def get_timestamped_result(job_id: str) -> list:
    client = get_client()
    result = client.get_job_result(job_id, include_timestamps=True)
    return result.get("segments", [])
