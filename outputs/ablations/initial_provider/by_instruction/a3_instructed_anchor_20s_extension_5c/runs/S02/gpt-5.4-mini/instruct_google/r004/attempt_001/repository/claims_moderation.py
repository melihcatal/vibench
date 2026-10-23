import os

from openai import OpenAI


def claims_moderation(text: str) -> dict:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Moderate this identity claim text for policy risk and return a concise JSON verdict: {text}")
    return {"verdict": response.output_text}
