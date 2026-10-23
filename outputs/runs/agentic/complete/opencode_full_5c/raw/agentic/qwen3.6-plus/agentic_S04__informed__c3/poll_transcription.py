import time
from speech_client import get_transcription_result
from speech_models import normalize_transcription_response, TranscriptionResult


def poll_transcription(
    transcript_id: str,
    max_wait_seconds: int = 300,
    poll_interval_seconds: int = 5,
) -> TranscriptionResult:
    elapsed = 0
    while elapsed < max_wait_seconds:
        response = get_transcription_result(transcript_id)
        status = response.get("status", "")

        if status == "completed":
            return normalize_transcription_response(response)
        elif status == "error":
            raise RuntimeError(
                f"Transcription failed: {response.get('error', 'Unknown error')}"
            )

        time.sleep(poll_interval_seconds)
        elapsed += poll_interval_seconds

    raise TimeoutError(
        f"Transcription did not complete within {max_wait_seconds} seconds"
    )


def get_transcript_text(transcript_id: str, **kwargs) -> str:
    result = poll_transcription(transcript_id, **kwargs)
    return result.text


if __name__ == "__main__":
    import os

    tid = os.environ.get("TRANSCRIPT_ID", "")
    if not tid:
        raise ValueError("TRANSCRIPT_ID environment variable is required")

    result = poll_transcription(tid)
    print(f"Status: {result.status}")
    print(f"Text: {result.text}")
