import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def retrieval_audio_brief(text: str, output_file: str = "brief.mp3") -> str:
    audio = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_monolingual_v1"
    )
    save(audio, output_file)
    return output_file