import os
from openai import OpenAI

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using OpenAI's Whisper API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text
