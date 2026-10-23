import base64
from typing import Any, Dict

from model_client import get_client, resolve_voice
from select_platform_resource import select_platform_resource


def platform_brief_audio(text: str, voice: str | None = None) -> Dict[str, Any]:
    resource = select_platform_resource("audio")
    client = get_client()
    response = client.audio.speech.create(
        model=resource["resource_id"],
        voice=resolve_voice(voice),
        input=text,
        format="mp3",
    )
    audio_bytes = response.read()
    return {
        "provider": "openai",
        "model": resource["resource_id"],
        "voice": resolve_voice(voice),
        "audio_base64": base64.b64encode(audio_bytes).decode("ascii"),
        "bytes": len(audio_bytes),
    }
