from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from model_client import get_openai_client, pick_model


def check_prompt_safety(prompt: str, generated_text: str = "") -> Dict[str, Any]:
    client: OpenAI = get_openai_client()
    response = client.moderations.create(
        model=pick_model(family="safety"),
        input=[prompt, generated_text],
    )
    result = response.results[0]
    return {
        "model": response.model,
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "category_scores": result.category_scores.model_dump(),
    }
