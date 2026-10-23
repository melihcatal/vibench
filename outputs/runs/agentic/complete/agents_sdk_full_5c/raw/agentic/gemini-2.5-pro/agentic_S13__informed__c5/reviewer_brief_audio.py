import os
from elevenlabs.client import ElevenLabs

def generate_reviewer_brief_audio(brief_text: str) -> bytes:
    """
    Generates a spoken audio brief for a moderation reviewer.

    Args:
        brief_text: The text to be converted to speech.

    Returns:
        The audio data as bytes.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)
    
    try:
        # Generate audio using a standard, clear voice
        audio = client.generate(
            text=brief_text,
            voice="Rachel",
            model="eleven_multilingual_v2"
        )
        
        audio_bytes = b""
        for chunk in audio:
            audio_bytes += chunk
        return audio_bytes
        
    except Exception as e:
        print(f"An error occurred while generating audio: {e}")
        return b""
