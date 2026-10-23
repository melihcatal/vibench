from __future__ import annotations

from model_client import get_azure_openai_client, get_tts_deployment
from model_models import AudioResult



def platform_brief_audio(text: str, voice: str = "alloy", audio_format: str = "mp3") -> AudioResult:
    client = get_azure_openai_client()
    deployment = get_tts_deployment()
    response = client.audio.speech.create(
        model=deployment,
        voice=voice,
        input=text,
        format=audio_format,
    )
    audio_base64 = getattr(response, "audio", None)
    if audio_base64 is None and hasattr(response, "model_dump"):
        payload = response.model_dump()
        audio_base64 = payload.get("audio") or payload.get("data")
    return AudioResult(
        audio_base64=audio_base64 or "",
        format=audio_format,
        voice=voice,
        raw=response,
    )
