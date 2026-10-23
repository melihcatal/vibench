from __future__ import annotations

from speech_client import get_elevenlabs_client, get_tts_defaults, iter_audio_chunks
from speech_models import AudioResult, TTSRequest


def synthesize_text(request: TTSRequest) -> AudioResult:
    defaults = get_tts_defaults()
    voice_id = request.voice_id or defaults["voice_id"]
    model_id = request.model_id or defaults["model_id"]
    client = get_elevenlabs_client()
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=request.text,
        output_format=request.output_format,
    )
    return AudioResult(
        audio_bytes=iter_audio_chunks(audio),
        content_type="audio/mpeg",
        provider="ElevenLabs",
        voice_id=voice_id,
        model_id=model_id,
    )
