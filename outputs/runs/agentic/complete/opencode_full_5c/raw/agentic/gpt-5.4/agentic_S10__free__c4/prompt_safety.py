from __future__ import annotations

from model_client import get_openai_client, select_model


def check_prompt_safety(prompt: str, generated_text: str = "") -> dict:
    client = get_openai_client()
    moderation_model = select_model("safety")
    response = client.moderations.create(
        model=moderation_model,
        input=[prompt, generated_text] if generated_text else [prompt],
    )
    results = []
    for item in response.results:
        results.append(
            {
                "flagged": item.flagged,
                "categories": item.categories.model_dump()
                if hasattr(item.categories, "model_dump")
                else {},
                "category_scores": item.category_scores.model_dump()
                if hasattr(item.category_scores, "model_dump")
                else {},
            }
        )
    return {"model": moderation_model, "results": results}
