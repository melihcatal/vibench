from typing import List
import openai

from safety_client import get_openai_client
from safety_models import ModerationResponse, SafetyDecision, SafetyCategory


def moderate_batch(texts: List[str]) -> ModerationResponse:
    """
    Moderates a batch of text messages using OpenAI's moderation API.
    """
    client = get_openai_client()
    if not client:
        return ModerationResponse(
            decisions=[
                SafetyDecision(
                    text=t,
                    is_safe=False,
                    reason="OpenAI client not configured",
                    categories=[],
                )
                for t in texts
            ]
        )

    try:
        response = client.moderations.create(input=texts, model="text-moderation-latest")
        
        decisions = []
        for i, res in enumerate(response.results):
            categories = []
            if res.flagged:
                for category, flagged in res.categories.model_dump().items():
                    if flagged:
                        categories.append(
                            SafetyCategory(
                                category=category.replace("_", " ").title(),
                                score=res.category_scores.model_dump().get(category, 0.0),
                                threshold=None,
                            )
                        )
            
            decision = SafetyDecision(
                text=texts[i],
                is_safe=not res.flagged,
                reason=", ".join(c.category for c in categories) or "Safe",
                categories=categories
            )
            decisions.append(decision)

        return ModerationResponse(decisions=decisions)

    except openai.APIError as e:
        return ModerationResponse(
            decisions=[
                SafetyDecision(
                    text=t, is_safe=False, reason=f"API Error: {e}", categories=[]
                )
                for t in texts
            ]
        )
