from typing import Optional
from openai import OpenAI


def runbook_translate(text: str, target_language: str = "es", model: str = "gpt-4.1-mini") -> str:
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=f"Translate the following secret-rotation runbook to {target_language}: {text}",
    )
    return response.output_text
