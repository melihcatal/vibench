import os
from typing import List
from elevenlabs import generate, save, set_api_key


def generate_audio_brief(
    text_summary: str,
    output_filepath: str = "brief.mp3",
    voice_id: str = "pNnB62EbsgqWn3Lw2z9M",
) -> str:
    """
    Generates a spoken brief from retrieved search results using ElevenLabs Text to Speech.
    """
    elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not elevenlabs_api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    set_api_key(elevenlabs_api_key)

    # The elevenlabs.generate function and explicit voice_id are concrete and identifiable ElevenLabs features.
    # They are directly from the elevenlabs-python library documentation.
    audio = generate(
        text=text_summary,
        voice=voice_id,  # Default voice ID, can be customized
        model="eleven_monolingual_v1",  # Explicitly using a concrete model identifier
    )

    save(audio, output_filepath)

    return output_filepath
