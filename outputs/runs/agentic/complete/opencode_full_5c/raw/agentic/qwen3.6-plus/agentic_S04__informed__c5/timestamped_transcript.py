import requests
from speech_client import SpeechConfig, build_timestamp_payload, get_assemblyai_headers
from speech_models import (
    TranscriptionResult,
    TranscriptionStatus,
    normalize_assemblyai_response,
    WordInfo,
)

ASSEMBLYAI_API_URL = "https://api.assemblyai.com/v2/transcript"


def get_timestamped_transcript(
    audio_url: str,
    config: SpeechConfig | None = None,
    language_code: str = "en",
    punctuate: bool = True,
    word_boost: list[str] | None = None,
) -> TranscriptionResult:
    cfg = config or SpeechConfig()
    payload = build_timestamp_payload(
        audio_url=audio_url,
        config=cfg,
        language_code=language_code,
        punctuate=punctuate,
        word_boost=word_boost or [],
    )

    response = requests.post(
        ASSEMBLYAI_API_URL,
        json=payload,
        headers=get_assemblyai_headers(cfg),
        timeout=30,
    )
    response.raise_for_status()
    raw = response.json()

    result = normalize_assemblyai_response(raw)
    return result


def get_timestamped_result(
    transcription_id: str,
    config: SpeechConfig | None = None,
) -> TranscriptionResult:
    cfg = config or SpeechConfig()
    endpoint = f"{ASSEMBLYAI_API_URL}/{transcription_id}"
    headers = get_assemblyai_headers(cfg)

    response = requests.get(endpoint, headers=headers, timeout=30)
    response.raise_for_status()
    raw = response.json()

    result = normalize_assemblyai_response(raw)

    if result.status != TranscriptionStatus.COMPLETED:
        raise ValueError(
            f"Transcription {transcription_id} is not completed (status: {result.status.value})"
        )

    return result


def extract_word_timestamps(result: TranscriptionResult) -> list[dict]:
    timestamps = []
    for word in result.words:
        timestamps.append(
            {
                "text": word.text,
                "start_ms": word.start_ms,
                "end_ms": word.end_ms,
                "confidence": word.confidence,
            }
        )
    return timestamps


if __name__ == "__main__":
    import sys

    audio_url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/audio.mp3"
    result = get_timestamped_transcript(audio_url)
    print(f"Transcription ID: {result.transcription_id}")
    print(f"Status: {result.status.value}")
    print(f"Word count: {len(result.words)}")
