import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_spoken_brief(text: str, output_path: str):
    """
    Generates a spoken audio brief from text using ElevenLabs API
    and saves it to a file.

    Args:
        text: The text to convert to speech.
        output_path: The file path to save the generated MP3 audio.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    
    # Provider-specific client class: elevenlabs.client.ElevenLabs
    client = ElevenLabs(api_key=api_key)

    # Generate audio from text
    # Provider-specific model/voice ID: "Rachel"
    audio = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )

    # Save the generated audio to a file
    save(audio, output_path)
    print(f"Audio saved to {output_path}")
