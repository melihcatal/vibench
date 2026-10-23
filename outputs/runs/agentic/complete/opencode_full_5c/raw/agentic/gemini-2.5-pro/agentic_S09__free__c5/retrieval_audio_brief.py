import os
from elevenlabs import generate, set_api_key


def retrieval_audio_brief(text_brief: str) -> bytes:
    """
    Generate a spoken brief from retrieved search results using ElevenLabs.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")
    set_api_key(api_key)

    audio = generate(text=text_brief, voice="Rachel", model="eleven_multilingual_v2")
    return audio
