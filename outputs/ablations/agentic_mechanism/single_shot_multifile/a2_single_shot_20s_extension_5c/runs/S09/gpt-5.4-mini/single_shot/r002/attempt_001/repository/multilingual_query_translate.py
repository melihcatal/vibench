import os
from typing import List

from openai import OpenAI


TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


def translate_queries(queries: List[str], target_language: str = "en", api_key: str | None = None) -> List[str]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    prompt = f"Translate each query to {target_language}. Return a JSON array of strings in the same order."
    response = client.chat.completions.create(model=TRANSLATION_MODEL, messages=[{"role": "system", "content": prompt}, {"role": "user", "content": "\n".join(queries)}], temperature=0)
    content = response.choices[0].message.content or "[]"
    import json
    return json.loads(content)
