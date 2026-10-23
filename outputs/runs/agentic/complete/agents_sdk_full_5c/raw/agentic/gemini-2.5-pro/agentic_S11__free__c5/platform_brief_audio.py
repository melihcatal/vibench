import os
from elevenlabs.client import ElevenLabs

def generate_audio_briefing(text: str, output_path: str):
    """
    Generates a spoken briefing from platform output text using ElevenLabs.

    Args:
        text: The text to convert to speech.
        output_path: The file path to save the generated MP3 audio.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
        
    # ElevenLabs is a third-party provider for text-to-speech services.
    client = ElevenLabs(api_key=api_key)
    
    # Generate audio using a specific voice and model from the ElevenLabs API
    audio = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )
    
    with open(output_path, "wb") as f:
        f.write(audio)

    print(f"Audio briefing saved to {output_path}")
