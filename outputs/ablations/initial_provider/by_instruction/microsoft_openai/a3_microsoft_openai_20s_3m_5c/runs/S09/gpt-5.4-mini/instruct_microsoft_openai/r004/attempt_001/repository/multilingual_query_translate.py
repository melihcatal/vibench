from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str):
    client = OpenAI()
    response = client.responses.create(model="gpt-4.1-mini", input=f"Translate to {target_language}: {query}")
    return response.output_text
