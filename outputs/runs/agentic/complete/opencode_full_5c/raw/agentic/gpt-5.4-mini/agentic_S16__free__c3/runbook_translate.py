import os

import openai


def runbook_translate(notes: str, target_language: str = "es"):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Translate this secret-rotation runbook to {target_language}: {notes}"
    result = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return result.output_text
