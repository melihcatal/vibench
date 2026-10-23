import requests
from speech_client import (
    SpeechConfig,
    build_diarization_payload,
    get_assemblyai_headers,
)
from speech_models import (
    TranscriptionResult,
    TranscriptionStatus,
    normalize_assemblyai_response,
)

ASSEMBLYAI_API_URL = "https://api.assemblyai.com/v2/transcript"


def request_diarized_transcript(
    audio_url: str,
    config: SpeechConfig | None = None,
    language_code: str = "en",
    punctuate: bool = True,
    format_text: bool = True,
) -> TranscriptionResult:
    cfg = config or SpeechConfig()
    payload = build_diarization_payload(
        audio_url=audio_url,
        config=cfg,
        language_code=language_code,
        punctuate=punctuate,
        format_text=format_text,
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


def get_diarized_transcript(
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


if __name__ == "__main__":
    import sys

    audio_url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/meeting.mp3"
    result = request_diarized_transcript(audio_url)
    print(f"Transcription ID: {result.transcription_id}")
    print(f"Status: {result.status.value}")
