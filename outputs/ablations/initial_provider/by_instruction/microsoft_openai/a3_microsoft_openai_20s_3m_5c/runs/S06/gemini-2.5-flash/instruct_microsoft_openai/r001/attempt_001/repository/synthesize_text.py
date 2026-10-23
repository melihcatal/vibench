from openai import OpenAI
import os

def synthesize_text(text: str) -> bytes:
    """
    Synthesizes plain text to an audio byte stream using OpenAI's TTS service.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    
    return response.content

