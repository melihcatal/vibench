import os
from safety_client import get_elevenlabs_client


def generate_reviewer_brief_audio(
    text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"
) -> bytes:
    """
    Generate spoken briefs for moderation reviewers using the ElevenLabs API.
    Saves the audio to a local file and returns the raw bytes.
    """
    elevenlabs = get_elevenlabs_client()

    audio = elevenlabs.generate(
        text=text,
        voice=elevenlabs.Voice(voice_id=voice_id),
        model="eleven_multilingual_v2",
    )

    # For demonstration, we'll also save it to a file.
    output_path = "reviewer_brief.mp3"
    elevenlabs.save(audio, output_path)

    return audio
