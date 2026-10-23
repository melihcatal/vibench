import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def reviewer_brief_audio(text: str, output_path: str):
    """
    Generates a spoken audio brief for a moderation reviewer.

    Args:
        text: The text content of the brief.
        output_path: The file path to save the generated MP3 audio file.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    try:
        client = ElevenLabs(api_key=api_key)
        
        # Generate audio using a standard, clear voice
        audio = client.generate(
            text=text,
            voice="Rachel", # A pre-made, professional voice
            model="eleven_multilingual_v2"
        )

        # Save the generated audio to the specified file path
        save(audio, output_path)
        print(f"Audio brief saved successfully to {output_path}")

    except Exception as e:
        print(f"An error occurred during audio generation: {e}")
        raise
