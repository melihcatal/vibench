import os
from typing import Iterable, List

from openai import OpenAI


def translate_live_captions(chunks: Iterable[str], target_language: str) -> List[str]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    results = []
    for chunk in chunks:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": f"Translate to {target_language}. Return only the translation.",
                },
                {"role": "user", "content": chunk},
            ],
        )
        results.append(response.choices[0].message.content or "")
    return results
