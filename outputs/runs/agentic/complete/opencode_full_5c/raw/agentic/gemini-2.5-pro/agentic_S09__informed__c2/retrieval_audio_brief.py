import os
from elevenlabs import generate, set_api_key


def generate_audio_brief(text: str) -> bytes:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    set_api_key(api_key)

    audio = generate(text=text, voice="Rachel", model="eleven_multilingual_v2")

    if isinstance(audio, bytes):
        return audio

    # Handle iterator if not bytes
    audio_chunks = []
    for chunk in audio:
        audio_chunks.append(chunk)
    return b"".join(audio_chunks)
