from typing import Mapping

from openai import OpenAI


def moderate_claim_text(claims: Mapping[str, str]) -> dict:
    client = OpenAI()
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=" ".join(str(v) for v in claims.values() if v),
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
