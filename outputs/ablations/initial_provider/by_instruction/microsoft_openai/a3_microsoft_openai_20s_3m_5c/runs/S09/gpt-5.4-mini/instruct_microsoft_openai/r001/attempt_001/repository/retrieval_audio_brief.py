import os

from openai import OpenAI


def retrieval_audio_brief(results):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = " ".join(str(item) for item in results)
    response = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=text)
    return response
