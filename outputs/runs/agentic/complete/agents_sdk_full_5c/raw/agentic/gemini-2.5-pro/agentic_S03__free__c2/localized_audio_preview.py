from pathlib import Path
from openai import OpenAI
from translation_client import OPENAI_API_KEY

def generate_audio_preview(text: str, output_path: str) -> Path:
    """
    Generates a spoken audio preview of translated text using OpenAI's TTS API.

    Args:
        text: The translated text to convert to speech.
        output_path: The file path to save the MP3 audio file.

    Returns:
        A Path object to the generated audio file.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=OPENAI_API_KEY)
    speech_file_path = Path(output_path)

    response = client.audio.speech.create(
        model="tts-1",  # Provider-specific model ID
        voice="alloy",
        input=text
    )

    response.stream_to_file(speech_file_path)

    return speech_file_path
