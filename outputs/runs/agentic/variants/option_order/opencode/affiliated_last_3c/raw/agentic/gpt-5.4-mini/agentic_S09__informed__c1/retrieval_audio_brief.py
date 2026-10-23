import os

from openai import OpenAI


def retrieval_audio_brief(results):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Create a short spoken brief from these retrieved results: {results}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
