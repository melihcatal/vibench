import os
from elevenlabs.client import ElevenLabs

def generate_audio_brief(text: str, output_path: str = "retrieval_brief.mp3"):
    """
    Generates an audio file from text using the ElevenLabs API.

    Args:
        text: The text to convert to speech.
        output_path: The path to save the generated MP3 file.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
        
    client = ElevenLabs(api_key=api_key)

    # Generate audio from text
    audio = client.generate(
        text=text,
        voice="Rachel",  # A common, pre-made voice
        model="eleven_multilingual_v2"
    )

    # Save the generated audio to a file
    with open(output_path, "wb") as f:
        f.write(audio)
    
    print(f"Audio brief saved to {output_path}")

