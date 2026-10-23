import os
from openai import OpenAI

def synthesize_text(text: str) -> bytes:
    """
    Synthesizes plain text to an audio byte stream using OpenAI's TTS.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",  # You can choose a different voice, e.g., "onyx", "nova", "shimmer", "fable", "echo"
        input=text,
    )
    return response.content
