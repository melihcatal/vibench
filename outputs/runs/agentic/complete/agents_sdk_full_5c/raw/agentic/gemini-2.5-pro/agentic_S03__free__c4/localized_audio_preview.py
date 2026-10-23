import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

from translation_client import get_elevenlabs_api_key

def generate_audio_preview(text: str, output_path: str):
    """
    Generates a spoken audio preview of translated text using ElevenLabs.

    Args:
        text: The text to convert to speech.
        output_path: The file path to save the generated MP3 audio.
    """
    api_key = get_elevenlabs_api_key()
    client = ElevenLabs(api_key=api_key)

    # Predefined voice and model for consistency
    voice_id = "Rachel"
    model_id = "eleven_multilingual_v2"

    audio = client.generate(
        text=text,
        voice=voice_id,
        model=model_id
    )

    save(audio, output_path)
