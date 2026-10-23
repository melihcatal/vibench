import os

from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Translate the following query into {target_language}: {query}",
    )
    return {"translated_query": response.output_text}
