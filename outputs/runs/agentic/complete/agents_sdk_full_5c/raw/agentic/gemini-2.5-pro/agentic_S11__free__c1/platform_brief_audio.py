from elevenlabs.client import ElevenLabs
from model_client import ELEVENLABS_API_KEY

def generate_audio_briefing_elevenlabs(text: str) -> bytes:
    """
    Generates an audio briefing from text using ElevenLabs API.
    """
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    # Provider-specific client class: elevenlabs.client.ElevenLabs
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    # Provider-specific resource ID (voice ID) and model ID
    audio_stream = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )

    # The result is a generator of audio file bytes (e.g., MP3)
    audio_bytes = b"".join(chunk for chunk in audio_stream)
    
    return audio_bytes
