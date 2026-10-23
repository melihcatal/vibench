from __future__ import annotations

from speech_client import get_transcriber
from speech_models import SpeechRequest, normalize_transcript


def submit_transcription(request: SpeechRequest):
    transcriber = get_transcriber()
    config = {
        "speaker_labels": request.speaker_labels,
        "punctuate": request.punctuate,
        "format_text": request.format_text,
        "word_boost": None,
        "language_detection": True if not request.language_code else False,
    }
    if request.language_code:
        config["language_code"] = request.language_code
    if request.context:
        config["custom_spelling"] = [{"from": [request.context], "to": request.context}]

    transcript = transcriber.transcribe(request.audio_path or request.audio_url, config)
    return normalize_transcript(transcript)
