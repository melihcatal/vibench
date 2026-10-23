import os

from openai import OpenAI


def runbook_translate(notes: str, target_language: str):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(model="gpt-4.1-mini", input=f"Translate this secret rotation runbook into {target_language}:\n{notes}")
    return response.output_text
