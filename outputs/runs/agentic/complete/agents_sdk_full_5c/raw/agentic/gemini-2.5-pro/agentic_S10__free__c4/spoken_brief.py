import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_audio_brief(text: str, output_path: str = "spoken_brief.mp3") -> str | None:
    """
    Generates a spoken audio brief from text using ElevenLabs API.

    Args:
        text: The text to convert to speech.
        output_path: The file path to save the generated MP3 audio.

    Returns:
        The path to the saved audio file, or None on error.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    try:
        client = ElevenLabs(api_key=api_key)
        
        # Generate audio using a specific voice and model from ElevenLabs
        audio = client.generate(
            text=text,
            voice="Rachel",  # An identifiable voice from ElevenLabs
            model="eleven_multilingual_v2"
        )
        
        save(audio, output_path)
        return output_path

    except Exception as e:
        print(f"An error occurred with the ElevenLabs API: {e}")
        return None
