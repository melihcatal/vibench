import os
from openai import OpenAI


def retrieval_audio_brief(text_brief: str, output_file_path: str = "briefing.mp3"):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text_brief,
    )

    response.stream_to_file(output_file_path)
    return output_file_path
