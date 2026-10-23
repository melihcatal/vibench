import time
import requests
from speech_client import SpeechConfig, get_assemblyai_headers
from speech_models import (
    TranscriptionResult,
    TranscriptionStatus,
    normalize_poll_response,
)

ASSEMBLYAI_API_URL = "https://api.assemblyai.com/v2/transcript"


def poll_transcription(
    transcription_id: str,
    config: SpeechConfig | None = None,
    interval_seconds: int | None = None,
    max_attempts: int | None = None,
) -> TranscriptionResult:
    cfg = config or SpeechConfig()
    poll_interval = (
        interval_seconds
        if interval_seconds is not None
        else cfg.polling_interval_seconds
    )
    max_polls = max_attempts if max_attempts is not None else cfg.max_poll_attempts

    endpoint = f"{ASSEMBLYAI_API_URL}/{transcription_id}"
    headers = get_assemblyai_headers(cfg)

    for attempt in range(max_polls):
        response = requests.get(endpoint, headers=headers, timeout=30)
        response.raise_for_status()
        raw = response.json()

        result = normalize_poll_response(raw)

        if result.status == TranscriptionStatus.COMPLETED:
            return result
        if result.status == TranscriptionStatus.ERROR:
            return result

        time.sleep(poll_interval)

    raise TimeoutError(
        f"Transcription {transcription_id} did not complete within {max_polls * poll_interval} seconds"
    )


if __name__ == "__main__":
    import sys

    transcription_id = sys.argv[1] if len(sys.argv) > 1 else ""
    result = poll_transcription(transcription_id)
    print(f"Status: {result.status.value}")
    print(f"Text: {result.text}")
