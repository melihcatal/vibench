from pathlib import Path

from elevenlabs.client import ElevenLabs

from safety_client import get_elevenlabs_client

def generate_reviewer_briefing_audio(text: str, output_path: str) -> None:
    """
    Generates a spoken audio brief for a moderation reviewer using ElevenLabs.

    Args:
        text: The text content of the briefing.
        output_path: The file path to save the generated MP3 audio.
    """
    client = get_elevenlabs_client()
    if not client:
        raise ConnectionError("ElevenLabs client not configured. Check ELEVENLABS_API_KEY.")

    try:
        # Generate audio using a standard voice model
        # For a full list of voices, see the ElevenLabs API documentation
        audio = client.generate(
            text=text,
            voice="Rachel", # A pre-made voice model ID
            model="eleven_multilingual_v2"
        )

        # Ensure the output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(audio)
        
        print(f"Audio briefing saved to {output_path}")

    except Exception as e:
        print(f"An error occurred with ElevenLabs TTS: {e}")
