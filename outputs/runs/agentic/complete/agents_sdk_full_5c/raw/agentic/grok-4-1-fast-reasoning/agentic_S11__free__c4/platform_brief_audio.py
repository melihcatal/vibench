import os
from openai import OpenAI

def generate_platform_brief_audio(text: str, output_path: str, voice: str = "alloy", model: str = "tts-1"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )
    response.stream_to_file(output_path)
