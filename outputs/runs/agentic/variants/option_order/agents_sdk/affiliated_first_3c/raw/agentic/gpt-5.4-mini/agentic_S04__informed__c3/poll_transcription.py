import assemblyai as aai

from speech_client import load_speech_config
from speech_models import TranscriptionResponse, normalize_segments


def poll_transcription(transcription_id: str) -> TranscriptionResponse:
    config = load_speech_config()
    if not config.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    aai.settings.api_key = config.api_key
    transcript = aai.Transcript.get(transcription_id)
    transcript.wait_for_completion()
    return TranscriptionResponse(
        id=transcript.id,
        status=transcript.status,
        text=transcript.text or "",
        segments=normalize_segments(getattr(transcript, "utterances", []) or getattr(transcript, "words", [])),
    )
