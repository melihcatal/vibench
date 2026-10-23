from speech_client import get_transcription_result
from speech_models import (
    normalize_transcription_response,
    extract_segments_with_timestamps,
)


def get_timestamped_transcript(
    transcript_id: str,
    max_wait_seconds: int = 300,
    poll_interval_seconds: int = 5,
) -> list[dict]:
    import time

    elapsed = 0
    while elapsed < max_wait_seconds:
        response = get_transcription_result(transcript_id)
        status = response.get("status", "")

        if status == "completed":
            result = normalize_transcription_response(response)
            return extract_segments_with_timestamps(result)
        elif status == "error":
            raise RuntimeError(
                f"Timestamped transcription failed: {response.get('error', 'Unknown error')}"
            )

        time.sleep(poll_interval_seconds)
        elapsed += poll_interval_seconds

    raise TimeoutError(
        f"Transcription did not complete within {max_wait_seconds} seconds"
    )


def format_timestamped_segments(segments: list[dict]) -> str:
    lines = []
    for seg in segments:
        start_s = seg["start_ms"] / 1000.0
        end_s = seg["end_ms"] / 1000.0
        speaker_label = f"[{seg['speaker']}]" if seg.get("speaker") else ""
        lines.append(f"[{start_s:.2f}-{end_s:.2f}] {speaker_label} {seg['text']}")
    return "\n".join(lines)


if __name__ == "__main__":
    import os

    tid = os.environ.get("TRANSCRIPT_ID", "")
    if not tid:
        raise ValueError("TRANSCRIPT_ID environment variable is required")

    segments = get_timestamped_transcript(tid)
    print(format_timestamped_segments(segments))
