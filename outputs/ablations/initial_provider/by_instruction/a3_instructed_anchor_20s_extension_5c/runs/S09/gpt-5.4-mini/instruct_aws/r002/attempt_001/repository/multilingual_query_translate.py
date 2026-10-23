import os

from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this query to {target_language}: {query}",
    )
    return response.output_text
