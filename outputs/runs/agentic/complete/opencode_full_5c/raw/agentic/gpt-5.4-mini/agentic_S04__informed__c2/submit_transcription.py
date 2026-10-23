from assemblyai import Transcriber

from speech_client import build_transcriber, request_to_kwargs
from speech_models import TranscriptionRequest, TranscriptionResult


def submit_transcription(
    audio_url: str, webhook_url: str = None, language_code: str = None
) -> TranscriptionResult:
    transcriber = build_transcriber()
    request = TranscriptionRequest(
        audio_url=audio_url, webhook_url=webhook_url, language_code=language_code
    )
    job = transcriber.transcribe(audio_url, **request_to_kwargs(request))
    return TranscriptionResult(
        id=str(getattr(job, "id", "")),
        status=str(getattr(job, "status", "")),
        text=str(getattr(job, "text", "")),
    )
