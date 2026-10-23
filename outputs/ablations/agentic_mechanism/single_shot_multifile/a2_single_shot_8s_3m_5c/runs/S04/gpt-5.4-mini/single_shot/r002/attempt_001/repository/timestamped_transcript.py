from typing import Any, Dict, Optional

from openai import OpenAI

from speech_client import get_openai_client
from speech_models import normalize_transcription_result


def timestamped_transcript(transcription_id: str) -> Dict[str, Any]:
    client = get_openai_client()
    result = client.audio.transcriptions.retrieve(transcription_id)
    return normalize_transcription_result(result)
