import os
from elevenlabs import generate, play, set_api_key

def generate_audio_brief(text: str, voice_id: str = "pNlY4w2d4r1B6wz0W8w0") -> bytes:
    """Generates a spoken brief from retrieved search results using ElevenLabs Text to Speech."""
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    set_api_key(api_key)

    audio = generate(text=text, voice=voice_id, model="eleven_monolingual_v1")
    # The 'play' function is for local playback, usually we would return the audio bytes.
    # play(audio)
    return audio

