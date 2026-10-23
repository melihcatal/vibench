from safety_client import get_elevenlabs_client


def generate_reviewer_brief_audio(text: str, voice: str = "Rachel") -> bytes:
    """
    Generates a spoken brief for moderation reviewers using ElevenLabs API.
    """
    elevenlabs = get_elevenlabs_client()

    audio = elevenlabs.generate(text=text, voice=voice, model="eleven_multilingual_v2")

    return audio
