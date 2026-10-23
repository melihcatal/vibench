from elevenlabs.client import ElevenLabs
from elevenlabs import save
import os

def generate_reviewer_brief_audio(brief: str, output_path: str = "reviewer_brief.mp3") -> str:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.generate(
        text=brief,
        voice="Rachel",
        model="eleven_monolingual_v1"
    )
    save(audio, output_path)
    return output_path