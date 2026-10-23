import requests
from speech_client import (
    SpeechConfig,
    build_transcription_payload,
    get_assemblyai_headers,
)
from speech_models import (
    TranscriptionResult,
    TranscriptionStatus,
    normalize_assemblyai_response,
)

ASSEMBLYAI_API_URL = "https://api.assemblyai.com/v2/transcript"


def submit_transcription(
    audio_url: str,
    config: SpeechConfig | None = None,
    language_code: str = "en",
    punctuate: bool = True,
    format_text: bool = True,
    disfluencies: bool = False,
    word_boost: list[str] | None = None,
) -> TranscriptionResult:
    cfg = config or SpeechConfig()
    payload = build_transcription_payload(
        audio_url=audio_url,
        config=cfg,
        language_code=language_code,
        punctuate=punctuate,
        format_text=format_text,
        disfluencies=disfluencies,
        word_boost=word_boost,
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


if __name__ == "__main__":
    import sys

    audio_url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/audio.mp3"
    result = submit_transcription(audio_url)
    print(f"Transcription ID: {result.transcription_id}")
    print(f"Status: {result.status.value}")
