import os

from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Translate this query into {target_language} while preserving search intent: {query}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
