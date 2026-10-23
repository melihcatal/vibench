import os
from elevenlabs.client import ElevenLabs
from typing import Optional

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def generate_localized_audio_preview(text: str, output_path: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM", model_id: str = "eleven_multilingual_v2") -> None:
    """Generate MP3 audio preview of translated text."""
    audio_stream = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=model_id,
        output_format="mp3_44100_128"
    )
    with open(output_path, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)