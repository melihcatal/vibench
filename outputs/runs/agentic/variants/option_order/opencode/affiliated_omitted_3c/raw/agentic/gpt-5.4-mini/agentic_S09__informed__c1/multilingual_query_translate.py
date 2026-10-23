import os

from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    result = client.responses.create(
        model="gpt-4.1-mini", input=f"Translate to {target_language}: {query}"
    )
    return result.output_text
