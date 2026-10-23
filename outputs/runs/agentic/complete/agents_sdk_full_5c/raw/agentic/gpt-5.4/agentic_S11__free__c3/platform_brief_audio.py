from __future__ import annotations

import base64

from model_client import get_azure_openai_client
from model_models import AudioBrief
from select_platform_resource import select_platform_resource


def platform_brief_audio(text: str, voice: str = "alloy") -> AudioBrief:
    client = get_azure_openai_client()
    resource = select_platform_resource(task="audio")
    response = client.audio.speech.create(
        model=resource.deployment_name or resource.model_id,
        voice=voice,
        input=text,
        response_format="mp3",
    )
    audio_bytes = response.read()
    return AudioBrief(format="mp3", audio_bytes=audio_bytes, transcript=text, raw={"provider": "azure_openai", "model": resource.model_id, "audio_base64": base64.b64encode(audio_bytes).decode("ascii")})
