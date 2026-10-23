import os

from openai import OpenAI

OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"


def translate_query(query: str, target_language: str = "en") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_TRANSLATION_MODEL,
        input=f"Translate this search query into {target_language}: {query}",
    )
    return response.output_text
