import os
from elevenlabs.client import ElevenLabs

def generate_audio_brief(text_brief: str, output_path: str):
    """
    Generates a spoken audio brief from text using the ElevenLabs API
    and saves it to a file.

    Args:
        text_brief: The text to be converted to speech.
        output_path: The file path to save the generated MP3 audio.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
        
    client = ElevenLabs(api_key=api_key)

    audio = client.generate(
        text=text_brief,
        voice="Bella", # A pre-made voice from ElevenLabs
        model="eleven_multilingual_v2"
    )

    with open(output_path, "wb") as f:
        f.write(audio)

    print(f"Audio brief saved to {output_path}")
