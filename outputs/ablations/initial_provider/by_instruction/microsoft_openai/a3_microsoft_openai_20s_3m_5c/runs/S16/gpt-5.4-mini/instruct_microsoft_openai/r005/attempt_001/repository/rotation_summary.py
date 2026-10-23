import os

from openai import OpenAI


def summarize_rotation_status(notes: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Summarize this secret rotation status:\n{notes}")
    return response.output_text
