from __future__ import annotations

from model_client import DEFAULT_MODERATION_MODEL, get_openai_client


def check_prompt_safety(prompt: str, generated_text: str = "") -> dict:
    client = get_openai_client()
    response = client.moderations.create(
        model=DEFAULT_MODERATION_MODEL,
        input=[prompt, generated_text] if generated_text else [prompt],
    )
    results = []
    for item in response.results:
        results.append(
            {
                "flagged": item.flagged,
                "categories": dict(item.categories),
                "category_scores": dict(item.category_scores),
            }
        )
    return {"model": response.model, "results": results}
