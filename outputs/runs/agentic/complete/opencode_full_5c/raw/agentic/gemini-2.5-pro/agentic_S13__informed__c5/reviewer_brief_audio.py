import os
from elevenlabs.client import ElevenLabs
from safety_models import AudioResult


def generate_reviewer_audio(text: str, output_path: str) -> AudioResult:
    """
    Generates a spoken brief for a moderation reviewer using ElevenLabs.
    """
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

    except Exception as e:
        # Simple error handling for API or file writing issues
        return AudioResult(audio_file_path=f"Error generating audio: {str(e)}")

    return AudioResult(audio_file_path=output_path)
