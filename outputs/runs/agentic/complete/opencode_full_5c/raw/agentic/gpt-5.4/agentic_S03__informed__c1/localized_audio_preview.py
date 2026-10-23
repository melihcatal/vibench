from __future__ import annotations

from elevenlabs.client import ElevenLabs

from translation_client import get_elevenlabs_api_key


def localized_audio_preview(
    text: str,
    voice_id: str = "JBFqnCBsd6RMkjVDRZzb",
    model_id: str = "eleven_multilingual_v2",
) -> bytes:
    client = ElevenLabs(api_key=get_elevenlabs_api_key())
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        text=text,
        output_format="mp3_44100_128",
    )
    return b"".join(audio)
