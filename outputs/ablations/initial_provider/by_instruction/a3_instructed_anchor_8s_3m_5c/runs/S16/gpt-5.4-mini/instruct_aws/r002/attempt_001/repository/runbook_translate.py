import os

from openai import OpenAI


def runbook_translate():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = os.getenv("RUNBOOK_TEXT", "Rotate secrets and verify access.")
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate the following runbook notes into concise English: {text}")
    return response.output_text


if __name__ == "__main__":
    print(runbook_translate())
