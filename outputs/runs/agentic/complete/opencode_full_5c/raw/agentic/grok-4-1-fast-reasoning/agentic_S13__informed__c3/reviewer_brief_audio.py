import os
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


def reviewer_brief_audio(
    brief_text: str, output_path: str = "reviewer_brief.mp3", voice: str = "Rachel"
) -> str:
    audio = client.generate(text=brief_text, voice=voice, model="eleven_monolingual_v1")
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    return output_path
