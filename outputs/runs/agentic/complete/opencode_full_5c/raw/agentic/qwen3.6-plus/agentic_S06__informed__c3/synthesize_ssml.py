from speech_client import get_client
from speech_models import SSMLRequest, TTSResponse, normalize_ssml_request


def build_ssml(
    text: str,
    voice_id: str = "",
    speed: float = 1.0,
    pitch: float = 0.0,
    volume_db: float = 0.0,
) -> str:
    rate_str = f"{int(speed * 100)}%"
    pitch_str = f"{int(pitch * 100)}Hz" if pitch != 0 else "default"
    volume_str = f"{volume_db:+.1f}dB" if volume_db != 0 else "default"
    ssml = (
        f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis">'
        f'<voice name="{voice_id}">'
        f'<prosody rate="{rate_str}" pitch="{pitch_str}" volume="{volume_str}">'
        f"{text}"
        f"</prosody>"
        f"</voice>"
        f"</speak>"
    )
    return ssml


def synthesize_ssml(text: str, **kwargs) -> TTSResponse:
    client = get_client()
    req = normalize_ssml_request(text, **kwargs)
    ssml = build_ssml(
        text=req.text,
        voice_id=req.voice_id,
        speed=req.speed,
        pitch=req.pitch,
        volume_db=req.volume_db,
    )
    audio_generator = client.text_to_speech.convert_as_stream(
        voice_id=req.voice_id,
        model_id=req.model_id,
        output_format=req.output_format,
        text=ssml,
    )
    audio_bytes = b"".join(audio_generator)
    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        model_id=req.model_id,
        voice_id=req.voice_id,
        character_count=len(req.text),
    )
