import os
from typing import Optional

from elevenlabs.client import ElevenLabs


def synthesize_text(text: str, voice_id: Optional[str] = None, model_id: str = "eleven_multilingual_v2") -> bytes:
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    selected_voice_id = voice_id or os.environ.get("ELEVENLABS_VOICE_ID", "Rachel")
    audio = client.text_to_speech.convert(
        voice_id=selected_voice_id,
        model_id=model_id,
        text=text,
        output_format="mp3_44100_128",
    )
    if isinstance(audio, bytes):
        return audio
    return b"".join(audio)
