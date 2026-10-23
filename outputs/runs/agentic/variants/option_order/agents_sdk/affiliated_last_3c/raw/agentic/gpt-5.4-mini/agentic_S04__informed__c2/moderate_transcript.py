from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI


CLIENT = OpenAI()
MODEL = "gpt-4o-mini"


def moderate_transcript(texts: Iterable[str]) -> List[dict]:
    results = []
    for text in texts:
        response = CLIENT.moderations.create(
            model=MODEL,
            input=text,
        )
        results.append({
            "text": text,
            "flagged": response.results[0].flagged,
            "categories": response.results[0].categories.model_dump(),
        })
    return results
