import os

from openai import OpenAI


def compliance_note_translate(text: str, target_language: str = "en") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini", input=f"Translate to {target_language}: {text}"
    )
    return response.output_text
