import os

from openai import OpenAI


def generate_spoken_brief(retrieved_results):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        f"Create a brief spoken summary of these search results: {retrieved_results}"
    )
    response = client.responses.create(model="gpt-4.1-mini", input=prompt)
    return response.output_text
