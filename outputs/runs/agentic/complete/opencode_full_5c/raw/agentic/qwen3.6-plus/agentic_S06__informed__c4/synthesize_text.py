from speech_client import get_elevenlabs_client
from speech_models import TTSRequest, TTSResponse


def synthesize_text(
    text: str,
    voice_id: str,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> TTSResponse:
    client = get_elevenlabs_client()
    request = TTSRequest(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
        stability=stability,
        similarity_boost=similarity_boost,
    )
    audio_generator = client.text_to_speech.convert(
        voice_id=request.voice_id,
        output_format=request.output_format,
        text=request.text,
        model_id=request.model_id,
        voice_settings={
            "stability": request.stability,
            "similarity_boost": request.similarity_boost,
            "style": request.style,
            "use_speaker_boost": request.use_speaker_boost,
        },
    )
    audio_bytes = b"".join(chunk for chunk in audio_generator)
    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        model_id=model_id,
        voice_id=voice_id,
        character_count=len(text),
    )
