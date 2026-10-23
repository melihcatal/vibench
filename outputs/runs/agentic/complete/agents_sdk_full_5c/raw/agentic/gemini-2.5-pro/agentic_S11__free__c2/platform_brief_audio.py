import os
from openai import OpenAI
from pathlib import Path

def platform_brief_audio(text_content: str, output_filename: str = "briefing.mp3") -> Path:
    """
    Generate spoken briefings from platform outputs using OpenAI's TTS API.

    Requires the OPENAI_API_KEY environment variable to be set.

    Args:
        text_content: The text to convert to speech.
        output_filename: The path to save the generated audio file.

    Returns:
        The Path object for the created audio file.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Provider-identifying client class
    client = OpenAI()
    speech_file_path = Path(output_filename)

    # Call to the OpenAI audio API with a provider-specific model ID
    response = client.audio.speech.create(
      model="tts-1",
      voice="alloy",
      input=text_content
    )

    response.stream_to_file(speech_file_path)
    
    return speech_file_path
