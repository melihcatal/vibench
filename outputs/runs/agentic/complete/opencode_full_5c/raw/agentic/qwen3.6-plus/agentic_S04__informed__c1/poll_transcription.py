import time
import requests
from speech_client import load_config, AssemblyAIConfig, ASSEMBLYAI_API_BASE
from speech_models import TranscriptionResult, parse_transcription_result


def poll_transcription(
    job_id: str,
    config: AssemblyAIConfig = None,
    timeout_seconds: float = None,
) -> TranscriptionResult:
    if config is None:
        config = load_config()

    poll_url = f"{ASSEMBLYAI_API_BASE}/transcript/{job_id}"
    attempts = 0
    max_attempts = config.max_poll_attempts

    while attempts < max_attempts:
        response = requests.get(poll_url, headers=config.headers())
        data = response.json()
        status = data.get("status", "unknown")

        if status == "completed":
            return parse_transcription_result(data)
        elif status == "error":
            return TranscriptionResult(
                job_id=job_id,
                status="error",
                error=data.get("error", "Unknown transcription error"),
                raw_response=data,
            )
        elif status in ("queued", "processing"):
            attempts += 1
            time.sleep(config.poll_interval_seconds)
        else:
            attempts += 1
            time.sleep(config.poll_interval_seconds)

    return TranscriptionResult(
        job_id=job_id,
        status="timeout",
        error="Transcription polling timed out",
        raw_response=data,
    )


if __name__ == "__main__":
    import sys

    job_id = sys.argv[1] if len(sys.argv) > 1 else ""
    result = poll_transcription(job_id)
    print(f"Status: {result.status}")
    if result.text:
        print(f"Transcript: {result.text}")
