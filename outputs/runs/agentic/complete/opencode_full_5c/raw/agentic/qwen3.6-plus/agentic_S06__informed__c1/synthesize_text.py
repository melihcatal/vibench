import httpx
from speech_client import build_headers, ELEVENLABS_API_BASE
from speech_models import TTSRequest, TTSResponse


def synthesize_text(
    text: str,
    voice_id: str = "EXAVITQu4vr4xnSDxMaL",
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    style: float = 0.0,
    use_speaker_boost: bool = True,
    api_key: str = None,
) -> TTSResponse:
    request = TTSRequest(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
        stability=stability,
        similarity_boost=similarity_boost,
        style=style,
        use_speaker_boost=use_speaker_boost,
    )
    headers = build_headers(api_key)
    headers["Accept"] = "audio/mpeg"
    url = f"{ELEVENLABS_API_BASE}/text-to-speech/{voice_id}"
    with httpx.Client(timeout=120.0) as client:
        response = client.post(
            url,
            headers=headers,
            json=request.to_payload(),
        )
        response.raise_for_status()
        audio_bytes = response.content
    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        character_count=len(text),
        voice_id=voice_id,
        model_id=model_id,
    )
