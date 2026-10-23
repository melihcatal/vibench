import os

from openai import OpenAI


def retrieval_audio_brief(results: list[dict]) -> bytes:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    text = "; ".join(item.get("title", "") for item in results)
    speech = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=text)
    return speech.read()
