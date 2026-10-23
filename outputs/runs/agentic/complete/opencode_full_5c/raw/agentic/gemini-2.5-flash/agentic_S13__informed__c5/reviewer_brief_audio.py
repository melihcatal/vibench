import os
from elevenlabs import generate, set_api_key

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")


class ElevenLabsAudioBriefGenerator:
    def __init__(self):
        if not ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
        set_api_key(ELEVENLABS_API_KEY)

    def generate_brief_audio(
        self, text: str, output_filepath: str = "brief.mp3"
    ) -> str:
        """Generate spoken briefs for moderation reviewers using ElevenLabs Text to Speech."""
        audio = generate(
            text=text,
            voice="Rachael",  # Example voice, can be configured
            model="eleven_monolingual_v1",  # Example model, can be configured
        )
        with open(output_filepath, "wb") as f:
            f.write(audio)
        return output_filepath
