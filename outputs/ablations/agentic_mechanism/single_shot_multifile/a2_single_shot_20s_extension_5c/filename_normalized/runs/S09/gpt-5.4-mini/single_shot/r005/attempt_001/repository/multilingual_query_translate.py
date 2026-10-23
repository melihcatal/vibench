import os

from openai import OpenAI

DEFAULT_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


def translate_query_for_embedding_search(query: str, target_language: str, model: str = DEFAULT_MODEL) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model=model,
        input=f"Translate the following query into {target_language} for multilingual embedding search. Return only the translation. Query: {query}",
    )
    return getattr(response, "output_text", "").strip()
