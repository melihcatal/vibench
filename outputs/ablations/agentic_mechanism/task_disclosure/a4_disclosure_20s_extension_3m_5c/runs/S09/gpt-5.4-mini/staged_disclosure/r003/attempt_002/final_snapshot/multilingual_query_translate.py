import os
from typing import Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


class MultilingualQueryTranslator:
    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def translate(self, query: str, target_language: str = "en") -> str:
        if not query:
            return query
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": "Translate the user's query into the target language for semantic search. Return only the translated text.",
                },
                {
                    "role": "user",
                    "content": f"Translate this query to {target_language}: {query}",
                },
            ],
        )
        return response.output_text.strip()


def translate_query_for_embedding_search(query: str, target_language: str = "en") -> str:
    return MultilingualQueryTranslator().translate(query, target_language=target_language)
