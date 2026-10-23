import os
from openai import OpenAI


def rotation_summary(notes: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-4.1-mini", input=f"Summarize this secret rotation status:
{notes}")
    return response.output_text
