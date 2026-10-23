import os
from elevenlabs import generate
from elevenlabs.client import ElevenLabs

def generate_reviewer_brief_audio(brief_text: str, output_path: str):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required.")
    client = ElevenLabs(api_key=api_key)
    audio = generate(
        text=brief_text,
        voice="Rachel",
        model="eleven_monolingual_v1"
    )
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
