from openai import OpenAI

from database_client import get_openai_client


def record_text_safety(text):
    client: OpenAI = get_openai_client()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Assess whether this document text is unsafe: {text}")
    return response.output_text
