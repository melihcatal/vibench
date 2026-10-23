import os

from openai import OpenAI


def translate_payload_text(payload_text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini", input=f"Translate to {target_language}: {payload_text}"
    )
    return response.output_text
