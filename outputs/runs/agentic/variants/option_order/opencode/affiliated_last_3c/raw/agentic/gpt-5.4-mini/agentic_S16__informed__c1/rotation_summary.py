import os

from openai import OpenAI


def rotation_summary(notes: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini", input=f"Summarize secret rotation status:\n{notes}"
    )
    return response.output_text
