import os
from elevenlabs import ElevenLabs
from elevenlabs.client import ElevenLabs
from speech_client import get_elevenlabs_client
from speech_models import TTSRequest, TTSResponse


def synthesize_text(
    text: str,
    voice_id: str = None,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
) -> TTSResponse:
    client = get_elevenlabs_client()
    if voice_id is None:
        voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")

    audio_stream = client.generate(
        text=text,
        voice=voice_id,
        model=model_id,
        output_format=output_format,
    )

    audio_bytes = (
        b"".join(audio_stream) if hasattr(audio_stream, "__iter__") else audio_stream
    )

    return TTSResponse(
        audio_data=audio_bytes,
        voice_id=voice_id,
        model_id=model_id,
        format=output_format,
        provider="elevenlabs",
    )
