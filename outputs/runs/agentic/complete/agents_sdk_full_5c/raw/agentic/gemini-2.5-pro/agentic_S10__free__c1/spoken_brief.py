import os
from elevenlabs import generate, play, set_api_key
from model_client import ELEVENLABS_API_KEY

def create_spoken_brief(text_to_speak: str, play_audio: bool = False) -> bytes:
    """
    Generates a spoken brief from text using the ElevenLabs API.

    Args:
        text_to_speak: The text to convert to speech.
        play_audio: If True, plays the audio locally. For server use, this should be False.

    Returns:
        The audio data as bytes.
    """
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    set_api_key(ELEVENLABS_API_KEY)

    # Generate audio using a specific voice
    audio = generate(
        text=text_to_speak,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )

    if play_audio and isinstance(audio, bytes):
        play(audio)
    
    return audio
