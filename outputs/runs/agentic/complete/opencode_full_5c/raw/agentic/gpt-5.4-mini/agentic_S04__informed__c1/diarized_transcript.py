from speech_client import post_json
from speech_models import TranscriptionJobRequest, normalize_transcript_payload


def diarized_transcript(audio_url: str) -> dict:
    request = TranscriptionJobRequest(audio_url=audio_url, speaker_labels=True)
    payload = {
        "audio_url": request.audio_url,
        "speaker_labels": True,
        "punctuate": True,
        "format_text": True,
    }
    return normalize_transcript_payload(post_json("/transcript", payload)).raw or {}
