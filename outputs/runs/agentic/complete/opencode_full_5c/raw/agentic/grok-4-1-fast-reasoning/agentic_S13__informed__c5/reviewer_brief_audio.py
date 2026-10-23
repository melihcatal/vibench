import os
from elevenlabs.client import ElevenLabs


def reviewer_brief_audio(brief: str, output_path: str):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY required.")

    client = ElevenLabs(api_key=api_key)
    audio = client.generate(
        text=brief, voice="21m00Tcm4TlvDq8ikWAM", model="eleven_monolingual_v1"
    )
    with open(output_path, "wb") as f:
        f.write(audio)
