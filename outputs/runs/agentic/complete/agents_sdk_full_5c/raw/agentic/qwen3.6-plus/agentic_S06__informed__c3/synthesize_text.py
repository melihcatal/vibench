"""Synthesize plain text to an audio byte stream using ElevenLabs Text-to-Speech."""

import os
from typing import Optional

from elevenlabs import ElevenLabs, Voice
from elevenlabs.client import ElevenLabs as ElevenLabsClient

from speech_client import get_elevenlabs_client
from speech_models import TTSRequest, TTSResponse


def synthesize_text(
    text: str,
    voice_id: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
    api_key: Optional[str] = None,
) -> TTSResponse:
    """Synthesize plain text to an audio byte stream using ElevenLabs TTS.

    Args:
        text: The plain text to synthesize.
        voice_id: ElevenLabs voice ID. Defaults to "EXAVITQu4vr4xnSDxMaL" (Rachel).
        model_id: ElevenLabs model ID. Defaults to "eleven_multilingual_v2".
        api_key: Optional ElevenLabs API key. Falls back to ELEVENLABS_API_KEY env var.

    Returns:
        TTSResponse containing the audio bytes and metadata.
    """
    client = get_elevenlabs_client(api_key=api_key)

    target_voice_id = voice_id or "EXAVITQu4vr4xnSDxMaL"

    audio_generator = client.text_to_speech.convert(
        voice_id=target_voice_id,
        model_id=model_id,
        text=text,
        output_format="mp3_44100_128",
    )

    audio_bytes = b"".join(audio_generator)

    return TTSResponse(
        audio_data=audio_bytes,
        format="mp3",
        voice_id=target_voice_id,
        model_id=model_id,
    )


def synthesize_text_stream(
    text: str,
    voice_id: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
    api_key: Optional[str] = None,
) -> bytes:
    """Convenience wrapper that returns raw audio bytes for a text string.

    Args:
        text: The plain text to synthesize.
        voice_id: ElevenLabs voice ID.
        model_id: ElevenLabs TTS model identifier.
        api_key: Optional API key override.

    Returns:
        Raw MP3 audio bytes from ElevenLabs TTS.
    """
    response = synthesize_text(
        text=text, voice_id=voice_id, model_id=model_id, api_key=api_key
    )
    return response.audio_data
