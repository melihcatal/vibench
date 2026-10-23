import os
from elevenlabs.client import ElevenLabs


def generate_reviewer_brief_audio(text: str) -> bytes:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    try:
        audio = client.generate(
            text=text, voice="Rachel", model="eleven_multilingual_v2"
        )

        audio_bytes = b""
        for chunk in audio:
            audio_bytes += chunk
        return audio_bytes

    except Exception as e:
        print(f"An error occurred while generating audio: {e}")
        return b""
