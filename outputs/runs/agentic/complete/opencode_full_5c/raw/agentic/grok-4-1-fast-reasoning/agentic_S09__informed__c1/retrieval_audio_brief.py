import os
import elevenlabs
from typing import Optional


def retrieval_audio_brief(
    brief_text: str, output_path: Optional[str] = None, voice: str = "Rachel"
) -> str:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")

    elevenlabs.set_api_key(api_key)

    if output_path is None:
        output_path = "retrieval_brief.mp3"

    audio = elevenlabs.generate(
        text=brief_text, voice=voice, model="eleven_monolingual_v1"
    )

    elevenlabs.save(audio, output_path)
    return output_path
