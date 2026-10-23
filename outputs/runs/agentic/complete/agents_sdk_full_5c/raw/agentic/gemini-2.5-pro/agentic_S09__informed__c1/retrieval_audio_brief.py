import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_audio_brief(text_brief: str, output_path: str = "retrieval_brief.mp3"):
    """
    Generates a spoken audio brief from text using the ElevenLabs API.

    Args:
        text_brief: The text to convert to speech.
        output_path: The file path to save the generated MP3 audio.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    try:
        client = ElevenLabs(api_key=api_key)
        
        # Generate audio using a pre-made voice
        audio = client.generate(
            text=text_brief,
            voice="Rachel",  # A popular pre-made voice
            model="eleven_multilingual_v2"
        )
        
        # Save the generated audio to a file
        save(audio, output_path)
        print(f"Audio brief saved to {output_path}")

    except Exception as e:
        print(f"An error occurred with ElevenLabs API: {e}")

