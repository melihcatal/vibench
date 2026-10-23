import os

from openai import OpenAI


def record_text_safety(record):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Assess if this record contains unsafe user-generated text. Return JSON only: {record}")
    return response.output_text
