import os

from openai import OpenAI


def runbook_translate():
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    text = os.environ["RUNBOOK_TEXT"]
    target_language = os.environ.get("RUNBOOK_TARGET_LANGUAGE", "Spanish")
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate to {target_language}: {text}")
    return response.output_text
