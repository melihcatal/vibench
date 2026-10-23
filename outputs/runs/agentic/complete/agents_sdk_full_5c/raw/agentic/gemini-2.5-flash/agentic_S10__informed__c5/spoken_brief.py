import os
from elevenlabs import generate, save, set_api_key

def generate_spoken_brief(text: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL") -> str:
    """Generate a spoken brief from the model output using ElevenLabs."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    set_api_key(api_key)

    audio = generate(
        text=text,
        voice=voice_id,
        model="eleven_monolingual_v1"
    )

    output_filename = "spoken_brief.mp3"
    save(audio, output_filename)
    return output_filename
