from speech_client import (
    get_elevenlabs_client,
    get_default_voice_id,
    get_default_model_id,
    get_default_output_format,
)
from speech_models import TTSRequest, TTSResponse


def synthesize_text(
    text: str, voice_id: str = None, model_id: str = None, output_format: str = None
) -> TTSResponse:
    client = get_elevenlabs_client()
    voice_id = voice_id or get_default_voice_id()
    model_id = model_id or get_default_model_id()
    output_format = output_format or get_default_output_format()

    audio_stream = client.generate(
        text=text,
        voice=voice_id,
        model=model_id,
        output_format=output_format,
    )

    audio_bytes = b"".join(audio_stream)
    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        model_used=model_id,
        voice_used=voice_id,
    )


def synthesize_text_with_settings(request: TTSRequest) -> TTSResponse:
    client = get_elevenlabs_client()
    voice_id = request.voice_id or get_default_voice_id()

    voice_settings = {
        "stability": request.stability,
        "similarity_boost": request.similarity_boost,
        "style": request.style,
        "use_speaker_boost": request.use_speaker_boost,
    }

    audio_stream = client.generate(
        text=request.text,
        voice=voice_id,
        model=request.model_id,
        output_format=request.output_format,
        voice_settings=voice_settings,
    )

    audio_bytes = b"".join(audio_stream)
    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        model_used=request.model_id,
        voice_used=voice_id,
    )
