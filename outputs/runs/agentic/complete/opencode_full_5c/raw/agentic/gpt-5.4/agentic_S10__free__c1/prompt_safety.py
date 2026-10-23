from __future__ import annotations

from model_client import choose_model, get_client


def check_prompt_safety(prompt: str, generated_text: str = "") -> dict:
    model = choose_model("safety")
    response = get_client().moderations.create(
        model=model,
        input=[prompt, generated_text] if generated_text else [prompt],
    )
    results = []
    for item in response.results:
        results.append(
            {
                "flagged": item.flagged,
                "categories": item.categories.model_dump()
                if hasattr(item.categories, "model_dump")
                else dict(item.categories),
                "category_scores": item.category_scores.model_dump()
                if hasattr(item.category_scores, "model_dump")
                else dict(item.category_scores),
            }
        )
    return {"provider": "openai", "model": model, "results": results}
