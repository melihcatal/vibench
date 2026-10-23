import os
from elevenlabs.client import ElevenLabs

def generate_audio_briefing(text: str, output_path: str) -> str:
    """
    Generates a spoken audio file from text using the ElevenLabs API.

    Args:
        text: The text to convert to speech.
        output_path: The file path to save the generated MP3 audio.
    
    Returns:
        The path to the saved audio file.
        
    Requires the ELEVEN_API_KEY environment variable.
    """
    api_key = os.getenv("ELEVEN_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)
    
    audio = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )
    
    with open(output_path, "wb") as f:
        f.write(audio)
        
    return output_path
