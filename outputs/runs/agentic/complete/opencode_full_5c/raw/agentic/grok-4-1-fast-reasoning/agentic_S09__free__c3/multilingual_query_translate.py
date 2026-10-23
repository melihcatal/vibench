import os
from typing import List
from openai import OpenAI


def translate_query_to_english(query: str) -> str:
    """
    Translates queries to English before multilingual embedding search using OpenAI gpt-4o-mini.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = "gpt-4o-mini"
    prompt = f"""Translate the following query to natural English. Respond ONLY with the translated query, nothing else:

{query}"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.1,
    )
    return response.choices[0].message.content.strip()
