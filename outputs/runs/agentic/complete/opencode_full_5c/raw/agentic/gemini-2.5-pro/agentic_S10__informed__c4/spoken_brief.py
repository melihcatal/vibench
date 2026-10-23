import os
from elevenlabs import generate, save
from elevenlabs.client import ElevenLabs


def generate_spoken_brief(text: str, output_path: str = "briefing.mp3"):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    try:
        audio = client.generate(
            text=text, voice="Rachel", model="eleven_multilingual_v2"
        )
        if audio:
            save(audio, output_path)
            return output_path
        return None
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
