from typing import List, Dict, Any
import os
import requests
from gtts import gTTS
import tempfile


def generate_spoken_brief(
    retrieved_results: List[Dict[str, Any]], output_file: str = "brief.mp3"
) -> str:
    """
    Generates a spoken brief from retrieved search results using Google Text-to-Speech (gTTS).

    Args:
        retrieved_results: List of retrieved search results with text content.
        output_file: Output file path for the spoken brief. Defaults to "brief.mp3".

    Returns:
        str: Path to the generated audio file.
    """
    brief_text = "Here are the top results:\n"
    for idx, result in enumerate(retrieved_results[:3], 1):
        brief_text += f"Result {idx}: {result.get('text', '')}\n"

    tts = gTTS(text=brief_text, lang="en")
    tts.save(output_file)

    return output_file
