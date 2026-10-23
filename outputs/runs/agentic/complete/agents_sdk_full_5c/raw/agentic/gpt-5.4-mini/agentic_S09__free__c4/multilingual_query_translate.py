import os

from openai import OpenAI

OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_TRANSLATION_MODEL,
        input=[
            {"role": "system", "content": f"Translate the user query into {target_language}."},
            {"role": "user", "content": query},
        ],
    )
    return response.output_text
