from speech_client import post_json
from speech_models import TranscriptionJobRequest, normalize_transcript_payload


def timestamped_transcript(audio_url: str) -> dict:
    request = TranscriptionJobRequest(audio_url=audio_url)
    payload = {
        "audio_url": request.audio_url,
        "punctuate": True,
        "format_text": True,
        "word_boost": [],
    }
    payload["auto_chapters"] = False
    return normalize_transcript_payload(post_json("/transcript", payload)).raw or {}
