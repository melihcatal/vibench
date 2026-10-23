import os
from openai import OpenAI


def secret_label_safety(text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-4.1-mini", input=f"Assess whether this secret label or note is unsafe text. Reply with SAFE or UNSAFE and a brief reason:
{text}")
    return response.output_text
