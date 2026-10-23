from speech_client import create_client, load_config, apply_request_settings
from speech_models import TranscriptionRequest, TranscriptionResult


def submit_transcription(audio_url: str, language_code: str | None = None) -> TranscriptionResult:
    cfg = load_config()
    client = create_client(cfg)
    request = TranscriptionRequest(
        audio_url=audio_url,
        webhook_url=cfg.webhook_url,
        language_code=language_code or cfg.language_code,
        speaker_labels=cfg.speaker_labels,
        word_boost=cfg.word_boost or [],
    )
    transcript = client.transcribe(request.audio_url, config=apply_request_settings(request))
    return TranscriptionResult(
        job_id=str(getattr(transcript, "id", "")),
        status=str(getattr(transcript, "status", "")),
        text=str(getattr(transcript, "text", "") or ""),
        confidence=getattr(transcript, "confidence", None),
        raw=getattr(transcript, "json_response", None),
    )
