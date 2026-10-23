import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save


def generate_localized_audio_preview(
    translated_text: str, output_path: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"
) -> None:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.generate(
        text=translated_text, voice=voice_id, model="eleven_multilingual_v2"
    )
    save(audio, output_path)
