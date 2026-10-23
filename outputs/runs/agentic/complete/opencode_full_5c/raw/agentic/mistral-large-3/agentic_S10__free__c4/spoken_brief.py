import os
from typing import Optional, Dict, Any
from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO
from model_client import get_llm_client


def generate_spoken_brief(
    text: str, language: str = "en", output_format: str = "mp3"
) -> bytes:
    """
    Generates a spoken brief from the model output using Google Text-to-Speech (gTTS).

    Args:
        text: The input text to convert to speech.
        language: The language of the input text.
        output_format: The output audio format (e.g., mp3, wav).

    Returns:
        The audio data as bytes.
    """
    tts = gTTS(text=text, lang=language, slow=False)

    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)

    if output_format != "mp3":
        audio = AudioSegment.from_mp3(audio_bytes)
        output_bytes = BytesIO()
        audio.export(output_bytes, format=output_format)
        return output_bytes.getvalue()

    return audio_bytes.getvalue()
