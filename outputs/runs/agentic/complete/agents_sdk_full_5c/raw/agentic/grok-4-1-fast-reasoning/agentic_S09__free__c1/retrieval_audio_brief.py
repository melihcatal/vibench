import os
from openai import OpenAI

def retrieval_audio_brief(brief_text: str, output_path: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=brief_text
    )
    response.stream_to_file(output_path)
