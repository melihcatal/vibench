import os

from openai import OpenAI


def secret_label_safety(label: str, notes: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(model="gpt-4.1-mini", input=f"Check if this secret label or notes contain unsafe text. Label: {label}\nNotes: {notes}")
    return response.output_text
