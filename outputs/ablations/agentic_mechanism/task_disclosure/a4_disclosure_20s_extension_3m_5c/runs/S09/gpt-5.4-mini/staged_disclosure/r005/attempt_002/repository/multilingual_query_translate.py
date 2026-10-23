import os
from typing import List, Sequence

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def translate_query(query: str, target_language: str = "English") -> str:
    response = _client().responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate the user's search query into {target_language}. Return only the translation.",
            },
            {"role": "user", "content": query},
        ],
    )
    return response.output_text.strip()


def translate_queries(queries: Sequence[str], target_language: str = "English") -> List[str]:
    return [translate_query(query, target_language=target_language) for query in queries]


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if not args:
        raise SystemExit("usage: multilingual_query_translate.py <query> [query ...]")

    print(translate_queries(args))
