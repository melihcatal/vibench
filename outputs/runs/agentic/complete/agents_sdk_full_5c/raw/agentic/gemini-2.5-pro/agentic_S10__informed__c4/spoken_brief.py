import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def generate_spoken_brief(text: str, output_path: str = "briefing.mp3") -> None:
    """
    Generates a spoken audio file from text using the ElevenLabs API.

    Args:
        text: The text to convert to speech.
        output_path: The path to save the generated MP3 file.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    try:
        # Generate audio using a pre-made voice
        audio = client.generate(
            text=text,
            voice="Rachel",
            model="eleven_multilingual_v2"
        )
        
        # Save the generated audio to a file
        save(audio, output_path)
        print(f"Audio content written to file {output_path}")

    except Exception as e:
        print(f"An error occurred with the ElevenLabs API: {e}")

