import os
from elevenlabs.client import ElevenLabs

def generate_reviewer_briefing_audio(text_brief: str, output_path: str) -> str:
    """
    Generates a spoken audio brief for a moderation reviewer using ElevenLabs.

    Args:
        text_brief: The text content of the briefing.
        output_path: The file path to save the generated MP3 audio.

    Returns:
        The path where the audio file was saved.
    """
    api_key = os.getenv("ELEVEN_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)
    
    # Generate audio using a specific voice and model
    audio = client.generate(
        text=text_brief,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )

    with open(output_path, "wb") as f:
        f.write(audio)
        
    return output_path
