from typing import List
from elevenlabs import generate, save
import os


def generate_spoken_brief(text: str, output_path: str = "brief.mp3") -> str:
    """
    Generates a spoken brief from text using ElevenLabs Text-to-Speech.

    Args:
        text: Input text to convert to speech.
        output_path: Path to save the generated audio file (default: "brief.mp3").

    Returns:
        Path to the generated audio file.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    audio = generate(
        text=text, api_key=api_key, voice="Rachel", model="eleven_multilingual_v2"
    )
    save(audio, output_path)
    return output_path


def retrieval_audio_brief(
    results: List[str], output_path: str = "retrieval_brief.mp3"
) -> str:
    """
    Generates a spoken brief from retrieved search results using ElevenLabs Text-to-Speech.

    Args:
        results: List of retrieved search result texts.
        output_path: Path to save the generated audio file (default: "retrieval_brief.mp3").

    Returns:
        Path to the generated audio file.
    """
    brief_text = "Here are the retrieved results:\n\n" + "\n\n".join(results)
    return generate_spoken_brief(brief_text, output_path)
