"""Synthesize plain text to an audio byte stream using ElevenLabs TTS."""

import os
import requests
from typing import Optional

from speech_client import get_elevenlabs_api_key, TTSClientConfig
from speech_models import TTSRequest, TTSResponse, normalize_audio_format


ELEVENLABS_TTS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"


def synthesize_text(
    text: str,
    voice_id: Optional[str] = None,
    model_id: Optional[str] = None,
    output_format: str = "mp3",
) -> TTSResponse:
    """Synthesize plain text to audio bytes via ElevenLabs Text-to-Speech API.

    Args:
        text: Plain text to synthesize.
        voice_id: ElevenLabs voice ID (defaults to ELEVENLABS_VOICE_ID env var).
        model_id: ElevenLabs model ID (defaults to eleven_multilingual_v2).
        output_format: Audio output format (mp3, pcm, ogg, etc.).

    Returns:
        TTSResponse containing audio bytes and metadata.

    Raises:
        requests.HTTPError: If the ElevenLabs API returns an error status.
    """
    config = TTSClientConfig()
    api_key = get_elevenlabs_api_key()
    vid = voice_id or config.voice_id
    mid = model_id or config.model_id

    url = f"{ELEVENLABS_TTS_API_URL}/{vid}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }

    format_map = {
        "mp3": "mp3_44100_128",
        "pcm": "pcm_16000",
        "ogg": "ogg_44100",
        "flac": "flac_44100",
        "wav": "pcm_16000",
    }
    norm_fmt = normalize_audio_format(output_format)
    eleven_output = format_map.get(norm_fmt, format_map["mp3"])

    payload = {
        "text": text,
        "model_id": mid,
        "output_format": eleven_output,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=config.timeout)
    response.raise_for_status()

    audio_bytes = response.content
    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg" if norm_fmt == "mp3" else f"audio/{norm_fmt}",
        character_count=len(text),
        voice_name=vid,
        model_used=mid,
    )


if __name__ == "__main__":
    result = synthesize_text("Hello, this is a test of the ElevenLabs text-to-speech API.")
    print(f"Generated {len(result.audio_bytes)} bytes of audio for '{result.voice_name}'")
