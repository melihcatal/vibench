import os
from typing import Dict, List, Optional

import openai


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def _client() -> openai.OpenAI:
    return openai.OpenAI(api_key=OPENAI_API_KEY)


def check_corpus_text_before_embedding(text: str) -> Dict[str, object]:
    if not isinstance(text, str) or not text.strip():
        return {"safe": False, "reason": "empty_text", "categories": [], "category_scores": {}}

    client = _client()
    result = client.moderations.create(model=OPENAI_MODEL, input=text)
    item = result.results[0]

    categories: List[str] = [name for name, flagged in item.categories.model_dump().items() if flagged]
    category_scores: Dict[str, float] = item.category_scores.model_dump()

    return {
        "safe": not item.flagged,
        "reason": "ok" if not item.flagged else "flagged_by_moderation",
        "categories": categories,
        "category_scores": category_scores,
    }


def corpus_is_safe(texts: List[str]) -> Dict[str, object]:
    unsafe_indices: List[int] = []
    details: List[Dict[str, object]] = []

    for index, text in enumerate(texts):
        result = check_corpus_text_before_embedding(text)
        details.append(result)
        if not result["safe"]:
            unsafe_indices.append(index)

    return {
        "safe": not unsafe_indices,
        "unsafe_indices": unsafe_indices,
        "details": details,
    }
