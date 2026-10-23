import os

from openai import OpenAI


def rotation_summary(text: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(model="gpt-4.1-mini", input=f"Summarize this secret rotation status:\n{text}")
    return response.output_text
