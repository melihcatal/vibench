import os

from openai import OpenAI


def record_summary(record):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Summarize this record succinctly: {record}")
    return response.output_text
