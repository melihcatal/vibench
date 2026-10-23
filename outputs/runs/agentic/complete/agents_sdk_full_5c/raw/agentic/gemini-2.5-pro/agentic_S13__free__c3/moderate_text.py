import os
from typing import List, Optional

import cohere
from dotenv import load_dotenv

from safety_client import get_cohere_client
from safety_models import ModerationResponse, SafetyDecision, SafetyCategory


def moderate_text(text: str) -> ModerationResponse:
    """
    Moderates a single piece of text using Cohere's moderation API.
    """
    client = get_cohere_client()
    if not client:
        return ModerationResponse(
            decisions=[
                SafetyDecision(
                    text=text,
                    is_safe=False,
                    reason="Cohere client not configured",
                    categories=[],
                )
            ]
        )

    try:
        response = client.moderate(texts=[text], model="moderate-english-v3.0")
        moderation = response.results[0]

        categories = []
        if moderation.flagged:
            for category, flagged in moderation.category_scores.items():
                if flagged:
                    categories.append(
                        SafetyCategory(category=category, score=1.0, threshold=None)
                    )

        decision = SafetyDecision(
            text=text,
            is_safe=not moderation.flagged,
            reason=", ".join([cat.category for cat in categories]) if categories else "Safe",
            categories=categories,
        )
        return ModerationResponse(decisions=[decision])

    except cohere.errors.CohereError as e:
        return ModerationResponse(
            decisions=[
                SafetyDecision(
                    text=text, is_safe=False, reason=f"API Error: {e}", categories=[]
                )
            ]
        )

