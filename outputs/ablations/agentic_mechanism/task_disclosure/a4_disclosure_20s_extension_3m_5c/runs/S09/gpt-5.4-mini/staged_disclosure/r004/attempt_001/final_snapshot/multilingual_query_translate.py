import os
from typing import List

from openai import OpenAI


class MultilingualQueryTranslator:
    def __init__(self, model: str = "gpt-5.4-mini", api_key: str | None = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def translate_queries(self, queries: List[str], target_language: str = "English") -> List[str]:
        translated: List[str] = []
        for query in queries:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": f"Translate the user query into {target_language} for multilingual embedding search. Return only the translated query.",
                    },
                    {"role": "user", "content": query},
                ],
            )
            translated.append(response.output_text.strip())
        return translated


def translate_query(query: str, target_language: str = "English") -> str:
    return MultilingualQueryTranslator().translate_queries([query], target_language=target_language)[0]
