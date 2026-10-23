import os
from openai import OpenAI


def quality_summary(text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-4.1-mini", input=f"Summarize translation quality issues in this text: {text}")
    return response.output_text.strip()
