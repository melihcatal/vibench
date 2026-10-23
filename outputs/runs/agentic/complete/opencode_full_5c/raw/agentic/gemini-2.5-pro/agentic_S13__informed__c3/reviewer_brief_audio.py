import os
from elevenlabs.client import ElevenLabs


def generate_reviewer_brief_audio(text: str, output_path: str) -> bool:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    try:
        audio = client.generate(
            text=text, voice="Rachel", model="eleven_multilingual_v2"
        )

        with open(output_path, "wb") as f:
            f.write(audio)

        return True
    except Exception as e:
        print(f"An error occurred with ElevenLabs API: {e}")
        return False
