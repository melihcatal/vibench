from typing import Any, Dict

from openai import OpenAI

from speech_client import get_client
from speech_models import normalize_transcript


def poll_transcription(transcription_id: str) -> Dict[str, Any]:
    client: OpenAI = get_client()
    payload = client.audio.transcriptions.retrieve(transcription_id)
    return normalize_transcript(payload.model_dump()).__dict__
