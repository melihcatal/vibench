from __future__ import annotations

from speech_client import DEFAULT_MODEL_ID, DEFAULT_OUTPUT_FORMAT, DEFAULT_VOICE_ID, get_elevenlabs_client, iter_audio_bytes
from speech_models import AudioArtifact, TTSRequest, normalize_audio_content_type


def synthesize_text(request: TTSRequest) -> AudioArtifact:
    client = get_elevenlabs_client()
    voice_id = request.voice_id or DEFAULT_VOICE_ID
    model_id = request.model_id or DEFAULT_MODEL_ID
    output_format = request.output_format or DEFAULT_OUTPUT_FORMAT

    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=request.text,
        output_format=output_format,
        voice_settings={
            k: v
            for k, v in {
                "stability": request.stability,
                "similarity_boost": request.similarity_boost,
                "style": request.style,
                "use_speaker_boost": request.use_speaker_boost,
            }.items()
            if v is not None
        } or None,
    )
    audio_bytes = iter_audio_bytes(audio_stream)
    return AudioArtifact(
        audio_bytes=audio_bytes,
        content_type=normalize_audio_content_type(output_format),
        provider="ElevenLabs",
        model_id=model_id,
        voice_id=voice_id,
        metadata={"api": "elevenlabs.text_to_speech.convert"},
    )
