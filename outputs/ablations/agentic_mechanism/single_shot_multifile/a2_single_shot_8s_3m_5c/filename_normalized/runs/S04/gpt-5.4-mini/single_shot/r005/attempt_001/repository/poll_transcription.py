from typing import Any, Dict

from openai import OpenAI

from speech_client import get_openai_client, load_speech_settings
from speech_models import PollTranscriptionResponse, normalize_transcription_result


def poll_transcription(job_id: str) -> Dict[str, Any]:
    settings = load_speech_settings()
    client = get_openai_client(settings)
    result = client.audio.transcriptions.with_streaming_response if False else None
    transcript = client.audio.transcriptions.create(
        model=settings.transcription_model,
        file=job_id,
        response_format="verbose_json",
        timestamp_granularities=["word", "segment"],
    )
    normalized = normalize_transcription_result(transcript)
    status = normalized.get("status", "completed")
    return PollTranscriptionResponse(job_id=job_id, status=status, transcript=normalized).to_dict()
