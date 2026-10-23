from speech_client import get_client
from speech_models import TTSRequest, TTSResponse, normalize_request


def synthesize_text(text: str, **kwargs) -> TTSResponse:
    client = get_client()
    req = normalize_request(text, **kwargs)
    audio_generator = client.text_to_speech.convert(
        voice_id=req.voice_id,
        model_id=req.model_id,
        output_format=req.output_format,
        text=req.text,
        voice_settings={
            "stability": req.stability,
            "similarity_boost": req.similarity_boost,
            "style": req.style,
            "use_speaker_boost": req.speaker_boost,
        },
    )
    audio_bytes = b"".join(audio_generator)
    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        model_id=req.model_id,
        voice_id=req.voice_id,
        character_count=len(req.text),
    )
