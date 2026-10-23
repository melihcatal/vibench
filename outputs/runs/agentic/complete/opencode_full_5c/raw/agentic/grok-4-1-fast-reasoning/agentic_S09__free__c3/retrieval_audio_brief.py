import os
from openai import OpenAI


def generate_retrieval_audio_brief(
    brief_text: str, output_file: str = "retrieval_brief.mp3"
) -> str:
    """
    Generates a spoken brief from retrieved search results using OpenAI TTS-1.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model="tts-1", voice="alloy", input=brief_text
    )
    response.stream_to_file(output_file)
    return f"Audio brief saved to {output_file}"
