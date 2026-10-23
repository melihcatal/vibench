from __future__ import annotations

from typing import Dict, Optional

from elevenlabs import ElevenLabs


DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
DEFAULT_MODEL_ID = "eleven_multilingual_v2"


def platform_brief_audio(text: str, voice_id: str = DEFAULT_VOICE_ID, model_id: str = DEFAULT_MODEL_ID, output_path: Optional[str] = None) -> Dict[str, object]:
    client = ElevenLabs(api_key=__import__("os").environ["ELEVENLABS_API_KEY"])
    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128",
        text=text,
    )
    audio_bytes = b"".join(audio_stream)
    if output_path:
        with open(output_path, "wb") as file_obj:
            file_obj.write(audio_bytes)
    return {
        "provider": "ElevenLabs",
        "voice_id": voice_id,
        "model_id": model_id,
        "audio_bytes": audio_bytes,
        "output_path": output_path,
    }
