import os
import elevenlabs
from model_models import AudioResponse


def generate_audio_briefing(text_for_briefing: str) -> AudioResponse:
    """
    Generates spoken briefings from platform outputs using ElevenLabs.

    Args:
        text_for_briefing: The text to be converted to speech.

    Returns:
        An AudioResponse object containing the audio content in bytes.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    elevenlabs.set_api_key(api_key)

    audio = elevenlabs.generate(
        text=text_for_briefing, voice="Rachel", model="eleven_multilingual_v2"
    )

    if isinstance(audio, bytes):
        return AudioResponse(audio_content=audio)

    # Handle iterator if streaming
    audio_chunks = b"".join([chunk for chunk in audio])
    return AudioResponse(audio_content=audio_chunks)
