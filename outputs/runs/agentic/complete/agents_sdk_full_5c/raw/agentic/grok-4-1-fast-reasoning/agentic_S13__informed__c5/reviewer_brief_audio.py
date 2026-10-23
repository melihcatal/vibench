import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from typing import Optional

def reviewer_brief_audio(brief_text: str, output_path: Optional[str] = None) -> str:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required.")
    client = ElevenLabs(api_key=api_key)
    audio = client.generate(
        text=brief_text,
        voice="Rachel",
        model="eleven_monolingual_v1"
    )
    if output_path is None:
        output_path = "reviewer_brief.mp3"
    save(audio, output_path)
    return output_path