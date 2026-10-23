import os

from openai import OpenAI


def runbook_translate(text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Translate the following secret-rotation runbook into {target_language}: {text}",
    )
    return response.output_text
