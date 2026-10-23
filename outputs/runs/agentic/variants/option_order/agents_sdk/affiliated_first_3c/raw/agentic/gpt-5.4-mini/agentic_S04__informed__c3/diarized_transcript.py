from speech_client import configure_client
from speech_models import TranscriptionResponse, normalize_segments


def diarized_transcript(audio_source: str) -> TranscriptionResponse:
    transcriber = configure_client()
    transcript = transcriber.transcribe(
        audio_source,
        speaker_labels=True,
        auto_chapters=False,
    )
    return TranscriptionResponse(
        id=getattr(transcript, "id", ""),
        status=getattr(transcript, "status", "submitted"),
        text=getattr(transcript, "text", ""),
        segments=normalize_segments(getattr(transcript, "utterances", []) or getattr(transcript, "words", [])),
    )
