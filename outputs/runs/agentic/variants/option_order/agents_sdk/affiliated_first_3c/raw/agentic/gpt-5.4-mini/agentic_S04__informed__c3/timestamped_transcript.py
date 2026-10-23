from speech_client import configure_client
from speech_models import TranscriptionResponse, normalize_segments


def timestamped_transcript(audio_source: str, timestamps: bool = True) -> TranscriptionResponse:
    transcriber = configure_client()
    transcript = transcriber.transcribe(
        audio_source,
        speaker_labels=False,
        timestamps=timestamps,
    )
    return TranscriptionResponse(
        id=getattr(transcript, "id", ""),
        status=getattr(transcript, "status", "submitted"),
        text=getattr(transcript, "text", ""),
        segments=normalize_segments(getattr(transcript, "utterances", []) or getattr(transcript, "words", [])),
    )
