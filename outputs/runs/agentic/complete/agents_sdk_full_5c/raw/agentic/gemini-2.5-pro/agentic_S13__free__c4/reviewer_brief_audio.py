"""Generates a spoken audio brief for a moderation reviewer using ElevenLabs."""
from elevenlabs import save
from safety_client import get_elevenlabs_client

def generate_reviewer_audio_brief(brief_text: str, output_path: str):
    """
    Converts a text brief into an audio file for a human reviewer.

    Args:
        brief_text: The text to be converted to speech.
        output_path: The file path to save the generated MP3 audio file.
    """
    client = get_elevenlabs_client()
    
    # Generate the audio from the text
    audio = client.generate(
        text=brief_text,
        voice="Rachel",  # A pre-made, professional-sounding voice
        model="eleven_multilingual_v2"
    )
    
    # Save the generated audio to a file
    save(audio, output_path)
