import os
from typing import Any, Dict, Optional

from openai import OpenAI

from speech_client import get_openai_client, load_speech_settings
from speech_models import SubmitTranscriptionRequest, SubmitTranscriptionResponse, normalize_transcription_result


def submit_transcription(audio_file_path: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    settings = load_speech_settings()
    client = get_openai_client(settings)
    request = SubmitTranscriptionRequest(audio_file_path=audio_file_path, metadata=metadata or {})
    with open(request.audio_file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=settings.transcription_model,
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
            extra_body={"metadata": request.metadata},
        )
    normalized = normalize_transcription_result(response)
    return SubmitTranscriptionResponse(job_id=normalized.get("id") or normalized.get("job_id") or "", status=normalized.get("status", "completed"), transcript=normalized).to_dict()
