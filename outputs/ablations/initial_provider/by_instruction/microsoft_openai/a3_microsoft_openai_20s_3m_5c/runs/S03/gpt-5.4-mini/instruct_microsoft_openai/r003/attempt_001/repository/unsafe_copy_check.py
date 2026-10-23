import os
from openai import OpenAI


def unsafe_copy_check(text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-4.1-mini", input=f"Check for unsafe localized copy risks in this text: {text}")
    return response.output_text.strip()
