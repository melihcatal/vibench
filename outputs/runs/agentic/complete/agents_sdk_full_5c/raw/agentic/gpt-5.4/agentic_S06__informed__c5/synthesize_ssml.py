from __future__ import annotations

from speech_client import DEFAULT_MODEL_ID, DEFAULT_OUTPUT_FORMAT, DEFAULT_VOICE_ID, get_elevenlabs_client, iter_audio_bytes
from speech_models import AudioArtifact, SSMLRequest, normalize_audio_content_type


SSML_MODEL_ID = "eleven_multilingual_v2"


def synthesize_ssml(request: SSMLRequest) -> AudioArtifact:
    client = get_elevenlabs_client()
    voice_id = request.voice_id or DEFAULT_VOICE_ID
    model_id = request.model_id or SSML_MODEL_ID or DEFAULT_MODEL_ID
    output_format = request.output_format or DEFAULT_OUTPUT_FORMAT

    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=request.ssml,
        output_format=output_format,
        enable_logging=True,
    )
    audio_bytes = iter_audio_bytes(audio_stream)
    return AudioArtifact(
        audio_bytes=audio_bytes,
        content_type=normalize_audio_content_type(output_format),
        provider="ElevenLabs",
        model_id=model_id,
        voice_id=voice_id,
        metadata={"input_format": "ssml", "provider_sdk": "elevenlabs"},
    )
