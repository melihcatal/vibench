import os

from openai import OpenAI


def retrieval_audio_brief(retrieved_results):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Create a brief spoken summary of these search results:\n" + "\n".join(
        retrieved_results
    )
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice="alloy", input=prompt
    )
    return {"audio": response}
