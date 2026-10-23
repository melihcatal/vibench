import httpx
import os
from speech_client import get_default_voice_id, get_default_model_id
from speech_models import SSMLRequest, TTSResponse


def synthesize_ssml(
    ssml: str, voice_id: str = None, model_id: str = None, output_format: str = None
) -> TTSResponse:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")

    voice_id = voice_id or get_default_voice_id()
    model_id = model_id or get_default_model_id()
    output_format = output_format or "mp3_44100_128"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": ssml,
        "model_id": model_id,
        "output_format": output_format,
    }

    response = httpx.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    audio_bytes = response.content
    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        model_used=model_id,
        voice_used=voice_id,
    )


def synthesize_ssml_with_prosody(
    text: str,
    rate: str = "medium",
    pitch: str = "medium",
    volume: str = "medium",
    voice_id: str = None,
    model_id: str = None,
) -> TTSResponse:
    ssml = (
        "<speak>"
        f'<prosody rate="{rate}" pitch="{pitch}" volume="{volume}">'
        f"{text}"
        "</prosody>"
        "</speak>"
    )
    return synthesize_ssml(ssml, voice_id=voice_id, model_id=model_id)


def synthesize_ssml_request(request: SSMLRequest) -> TTSResponse:
    return synthesize_ssml(
        ssml=request.ssml,
        voice_id=request.voice_id,
        model_id=request.model_id,
        output_format=request.output_format,
    )
