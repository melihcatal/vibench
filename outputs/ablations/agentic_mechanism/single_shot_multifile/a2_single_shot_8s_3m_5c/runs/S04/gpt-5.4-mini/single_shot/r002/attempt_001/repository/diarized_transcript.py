from typing import Any, Dict, Optional

from openai import OpenAI

from speech_client import get_openai_client, resolve_audio_path
from speech_models import TranscriptionJobRequest, normalize_transcription_result


def diarized_transcript(audio_path: str, model: Optional[str] = None) -> Dict[str, Any]:
    client = get_openai_client()
    req = TranscriptionJobRequest(audio_path=audio_path, model=model, response_format="verbose_json")
    with resolve_audio_path(req.audio_path) as path:
        with open(path, "rb") as f:
            result = client.audio.transcriptions.create(file=f, model=req.model, response_format="verbose_json", timestamp_granularities=["segment"])
    return normalize_transcription_result(result)
