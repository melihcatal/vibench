import os
from typing import Optional

from openai import OpenAI


OPENAI_TRANSLATION_MODEL = "gpt-4.1-mini"


def translate_query(query: str, target_language: str = "en", source_language: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    system_prompt = (
        "You translate search queries for multilingual embedding search. "
        "Return only the translated query, preserving intent and named entities."
    )
    user_prompt = f"Translate this query to {target_language}."
    if source_language:
        user_prompt += f" The source language is {source_language}."
    user_prompt += f" Query: {query}"
    response = client.responses.create(
        model=OPENAI_TRANSLATION_MODEL,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.output_text.strip()
