from openai import OpenAI


def runbook_translate(notes: str, target_language: str = "es") -> str:
    client = OpenAI()
    response = client.responses.create(model="gpt-4.1-mini", input=f"Translate the following secret-rotation runbook notes to {target_language}: {notes}")
    return response.output_text
