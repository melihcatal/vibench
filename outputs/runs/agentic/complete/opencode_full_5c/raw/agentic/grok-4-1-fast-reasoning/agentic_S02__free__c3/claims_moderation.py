import os
import openai
from .identity_models import FreeTextClaim


def moderate_free_text_claim(claim: FreeTextClaim) -> dict:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="text-moderation-latest", input=claim.claim_text
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }
