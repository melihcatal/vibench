import os
from openai import OpenAI


def generate_platform_brief_audio(output: str, audio_path: str = "brief.mp3") -> None:
    """
    Generates spoken briefing audio from platform output using OpenAI TTS.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    speech_response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=output,
    )
    speech_response.stream_to_file(audio_path)
