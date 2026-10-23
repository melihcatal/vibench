import os
from elevenlabs.client import ElevenLabs

def generate_audio_briefing(text: str, output_path: str = "briefing.mp3"):
    """
    Generates a spoken audio briefing from text using ElevenLabs API.

    Args:
        text: The text to convert to speech.
        output_path: The path to save the generated MP3 file.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY must be set.")

    # Provider-specific client from the elevenlabs SDK
    client = ElevenLabs(api_key=api_key)

    # Generate audio using a specific voice ID, a provider signal
    audio = client.generate(
        text=text,
        voice="Rachel",  # Provider-specific voice model identifier
        model="eleven_multilingual_v2" # Provider-specific model identifier
    )

    with open(output_path, "wb") as f:
        f.write(audio)
    
    print(f"Audio briefing saved to {output_path}")

