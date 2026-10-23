import os
from elevenlabs.client import ElevenLabs

def generate_audio_brief(text_brief: str, output_path: str):
    """
    Generates a spoken audio brief from retrieved search results text
    using the ElevenLabs Text-to-Speech API.

    Args:
        text_brief: The text to be converted to speech.
        output_path: The file path to save the generated MP3 audio.
    """
    api_key = os.environ.get("ELEVEN_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    # Generate audio from the text brief
    # "Rachel" is one of ElevenLabs' pre-made voices.
    audio = client.generate(
        text=text_brief,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )

    # Save the generated audio to a file
    with open(output_path, "wb") as f:
        f.write(audio)
    
    print(f"Audio brief saved to {output_path}")
