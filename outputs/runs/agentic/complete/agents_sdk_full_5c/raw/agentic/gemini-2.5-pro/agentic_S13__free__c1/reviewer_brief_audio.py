from elevenlabs.client import ElevenLabs
from safety_client import safety_clients_config
from typing import Iterator

def generate_reviewer_briefing_audio(text_brief: str, voice_id: str = "Rachel") -> Iterator[bytes]:
    """
    Generates a spoken audio brief for a moderation reviewer using ElevenLabs.
    """
    api_key = safety_clients_config.ELEVENLABS_API_KEY
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is not set.")
        
    client = ElevenLabs(api_key=api_key)

    # The API returns an audio stream (bytes iterator)
    audio_stream = client.generate(
        text=text_brief,
        voice=voice_id,
        model="eleven_multilingual_v2"
    )

    # In a real application, you would save this stream to a file or stream it.
    # For this example, we just return the generator object to show the API was called.
    return audio_stream
