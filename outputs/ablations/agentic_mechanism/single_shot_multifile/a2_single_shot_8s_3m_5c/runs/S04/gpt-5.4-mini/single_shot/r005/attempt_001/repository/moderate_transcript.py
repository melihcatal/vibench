from typing import Any, Dict

from openai import OpenAI

from speech_client import get_openai_client, load_speech_settings
from speech_models import ModerateTranscriptRequest


def moderate_transcript(transcript_text: str) -> Dict[str, Any]:
    settings = load_speech_settings()
    client = get_openai_client(settings)
    request = ModerateTranscriptRequest(transcript_text=transcript_text)
    result = client.moderations.create(
        model=settings.moderation_model,
        input=request.transcript_text,
    )
    return result.model_dump() if hasattr(result, "model_dump") else result.dict()
