from openai import OpenAI

from database_client import get_openai_client


def record_translate(text, target_language):
    client: OpenAI = get_openai_client()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate this document text to {target_language}: {text}")
    return response.output_text
