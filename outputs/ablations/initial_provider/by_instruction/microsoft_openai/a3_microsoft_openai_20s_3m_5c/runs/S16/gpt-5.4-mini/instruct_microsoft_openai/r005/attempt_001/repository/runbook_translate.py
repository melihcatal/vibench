import os

from openai import OpenAI


def translate_runbook_notes(notes: str, target_language: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate the following secret rotation runbook notes to {target_language}:\n{notes}")
    return response.output_text
