from speech_client import configure_client, normalize_audio_source
from speech_models import TranscriptionRequest, TranscriptionResponse, normalize_segments


def submit_transcription(audio_source: str) -> TranscriptionResponse:
    transcriber = configure_client()
    request = TranscriptionRequest(audio_source=normalize_audio_source(audio_source))
    transcript = transcriber.transcribe(
        request.audio_source,
        webhook_url=request.webhook_url,
        language_code=request.language_code,
        speaker_labels=request.speaker_labels,
    )
    return TranscriptionResponse(
        id=getattr(transcript, "id", ""),
        status=getattr(transcript, "status", "submitted"),
        text=getattr(transcript, "text", ""),
        segments=normalize_segments(getattr(transcript, "utterances", []) or getattr(transcript, "words", [])),
    )
