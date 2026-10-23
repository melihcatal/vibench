from openai import OpenAI

from database_client import get_openai_client


def record_summary(record):
    client: OpenAI = get_openai_client()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Summarize this document record: {record}")
    return response.output_text
