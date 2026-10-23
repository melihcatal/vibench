from model_client import get_openai_client


def check_prompt_safety(text: str) -> dict:
    client = get_openai_client()
    resp = client.moderations.create(input=text, model="text-moderation-latest")
    result = resp.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": {k: float(v) for k, v in result.category_scores.items()},
    }
