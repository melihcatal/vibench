import os

from openai import OpenAI


def runbook_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key") or os.environ.get("OPENAI_API_KEY"))
    model = config.get("model", "gpt-4.1-mini")
    response = client.responses.create(model=model, input=f"Translate the following secret-rotation runbook notes to {payload.get('language', 'English')}: {payload.get('notes', '')}")
    return {"translation": response.output_text, "model": model}
