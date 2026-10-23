"""
Synthesizes speech and writes the audio to a local file using ElevenLabs.
"""
from elevenlabs import save
from speech_client import get_elevenlabs_client

def save_elevenlabs_audio(
    text: str,
    output_path: str,
    voice_id: str = "Rachel",
    model: str = "eleven_multilingual_v2"
):
    """
    Generates audio from text using ElevenLabs and saves it to a file.

    Args:
        text: The text to be synthesized.
        output_path: The path to save the resulting audio file (e.g., "speech.mp3").
        voice_id: The ElevenLabs voice ID to use.
        model: The ElevenLabs model to use for synthesis.
    """
    client = get_elevenlabs_client()

    audio = client.generate(
        text=text,
        voice=voice_id,
        model=model
    )

    if audio:
        save(audio, output_path)
        print(f"Audio content saved to {output_path}")
    else:
        raise IOError("Failed to generate audio from ElevenLabs.")
