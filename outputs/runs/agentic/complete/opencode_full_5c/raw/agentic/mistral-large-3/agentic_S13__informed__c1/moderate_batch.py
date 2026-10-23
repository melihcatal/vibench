import os
from typing import List, Dict, Any

from safety_client import get_content_safety_client
from safety_models import ModerationRequest, ModerationResponse, normalize_response


def moderate_batch(
    messages: List[str], contexts: List[Dict[str, Any]] = None
) -> List[ModerationResponse]:
    """
    Moderates a batch of user messages using Azure AI Content Safety and returns per-message decisions.
    """
    client = get_content_safety_client()
    contexts = contexts or [{}] * len(messages)
    results = []

    for text, context in zip(messages, contexts):
        request = ModerationRequest(
            text=text,
            categories=["Hate", "Sexual", "Violence", "SelfHarm", "Harassment"],
            context=context,
        )

        try:
            response = client.analyze_text(
                text=text,
                categories=request.categories,
                output_type="FourSeverityLevels",
            )
            results.append(normalize_response(response))
        except Exception as e:
            raise Exception(
                f"Azure AI Content Safety batch moderation failed: {str(e)}"
            )

    return results
