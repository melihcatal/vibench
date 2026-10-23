import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_reviewer_brief_audio(text: str, output_path: str):
    """
    Generates an audio file from text for a reviewer briefing using ElevenLabs API.
    
    Args:
        text: The text to convert to speech.
        output_path: The file path to save the generated MP3 audio.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    try:
        client = ElevenLabs(api_key=api_key)
        
        # Generate audio using a pre-made voice
        audio = client.generate(
            text=text,
            voice="Rachel", # A popular pre-made voice model from ElevenLabs
            model="eleven_multilingual_v2"
        )
        
        # Save the generated audio to a file
        save(audio, output_path)
        print(f"Audio briefing saved to {output_path}")

    except Exception as e:
        print(f"An error occurred while generating audio with ElevenLabs: {e}")
