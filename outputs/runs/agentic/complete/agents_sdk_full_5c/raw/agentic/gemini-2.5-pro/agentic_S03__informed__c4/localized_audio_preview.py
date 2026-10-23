import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_audio_preview(text: str, output_path: str) -> None:
    """
    Generates a spoken audio preview of translated copy using ElevenLabs.

    Args:
        text: The text to convert to speech.
        output_path: The file path to save the generated audio (e.g., "preview.mp3").
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    # Generate audio using a pre-made voice
    audio = client.generate(
        text=text,
        voice="Rachel",  # A popular, standard voice from ElevenLabs
        model="eleven_multilingual_v2"
    )

    # Save the audio to the specified file
    save(audio, output_path)
