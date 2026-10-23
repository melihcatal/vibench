import os

from openai import OpenAI


def record_translate(record, target_language):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate user-facing fields in this record to {target_language}: {record}")
    return response.output_text
