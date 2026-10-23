from __future__ import annotations

from elevenlabs import VoiceSettings

from speech_client import get_elevenlabs_client, get_tts_defaults, iter_audio_chunks
from speech_models import AudioResult, SSMLRequest, ssml_to_plain_text


def synthesize_ssml(request: SSMLRequest) -> AudioResult:
    defaults = get_tts_defaults()
    voice_id = request.voice_id or defaults["voice_id"]
    model_id = request.model_id or defaults["model_id"]
    text = ssml_to_plain_text(request.text)
    client = get_elevenlabs_client()
    settings = VoiceSettings(
        stability=request.stability if request.stability is not None else 0.45,
        similarity_boost=request.similarity_boost
        if request.similarity_boost is not None
        else 0.8,
        style=request.style if request.style is not None else 0.15,
        use_speaker_boost=request.use_speaker_boost
        if request.use_speaker_boost is not None
        else True,
    )
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=text,
        voice_settings=settings,
        output_format=request.output_format,
    )
    return AudioResult(
        audio_bytes=iter_audio_chunks(audio),
        content_type="audio/mpeg",
        provider="ElevenLabs",
        voice_id=voice_id,
        model_id=model_id,
    )
