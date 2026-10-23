import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_localized_audio_preview(text: str, lang: str, output_path: str):
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.generate(
        text=text,
        voice="21m00Tcm4TlvDq8ikWAM",  # Multilingual voice like Rachel
        model="eleven_multilingual_v2",
        output_format="mp3_22050_32",
    )
    save(audio, output_path)
