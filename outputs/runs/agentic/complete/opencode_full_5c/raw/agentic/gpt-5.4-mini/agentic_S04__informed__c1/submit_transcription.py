from speech_client import post_json
from speech_models import TranscriptionJobRequest, normalize_transcript_payload


def submit_transcription(audio_url: str, webhook_url: str | None = None) -> dict:
    request = TranscriptionJobRequest(audio_url=audio_url, webhook_url=webhook_url)
    payload = {
        "audio_url": request.audio_url,
        "speaker_labels": request.speaker_labels,
        "punctuate": request.punctuate,
        "format_text": request.format_text,
    }
    if request.webhook_url:
        payload["webhook_url"] = request.webhook_url
    return normalize_transcript_payload(post_json("/transcript", payload)).raw or {}
