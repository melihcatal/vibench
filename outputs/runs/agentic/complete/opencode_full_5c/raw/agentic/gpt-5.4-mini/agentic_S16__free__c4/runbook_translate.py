import os

from openai import OpenAI


def runbook_translate(text: str, target_language: str = "es") -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-4.1-mini", input=f"Translate to {target_language}: {text}"
    )
    return response.output_text
