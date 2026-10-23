import openai
import os
from typing import Optional


def localized_audio_preview(
    text: str, output_file: str, voice: Optional[str] = "alloy"
) -> str:
    """
    Generate a spoken audio preview of translated text using OpenAI TTS-1.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    speech_response = client.audio.speech.create(model="tts-1", voice=voice, input=text)
    with open(output_file, "wb") as file:
        file.write(speech_response.content)
    return output_file
