import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save


def generate_reviewer_brief_audio(brief_text: str, output_path: str):
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.generate(
        text=brief_text,
        voice="21m00Tcm4TlvDq8ikWAM",  # Rachel
        model="eleven_monolingual_v1",
    )
    save(audio, output_path)
