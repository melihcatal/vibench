import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_audio_brief(text_summary: str, output_path: str) -> str:
    """
    Generates a spoken audio brief from a text summary using ElevenLabs API.

    Args:
        text_summary: The text to convert to speech.
        output_path: The file path to save the generated MP3 audio.

    Returns:
        The path to the saved audio file.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    try:
        # Provider-identifying client class
        client = ElevenLabs(api_key=api_key)
        
        # Generate audio using a specific voice model
        audio = client.generate(
            text=text_summary,
            voice="Rachel",
            model="eleven_multilingual_v2"
        )
        
        # Save the generated audio to a file
        save(audio, output_path)
        
        return output_path
    except Exception as e:
        raise RuntimeError(f"ElevenLabs API error: {e}")

