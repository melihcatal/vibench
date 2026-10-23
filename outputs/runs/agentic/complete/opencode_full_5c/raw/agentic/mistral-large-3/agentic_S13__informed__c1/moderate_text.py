import os
import json
from typing import Dict, Any

from safety_client import get_content_safety_client
from safety_models import ModerationRequest, ModerationResponse, normalize_response


def moderate_text(text: str, context: Dict[str, Any] = None) -> ModerationResponse:
    """
    Scores user text for unsafe or policy-violating content using Azure AI Content Safety.
    """
    client = get_content_safety_client()
    request = ModerationRequest(
        text=text,
        categories=["Hate", "Sexual", "Violence", "SelfHarm", "Harassment"],
        context=context or {},
    )

    try:
        response = client.analyze_text(
            text=text, categories=request.categories, output_type="FourSeverityLevels"
        )
        return normalize_response(response)
    except Exception as e:
        raise Exception(f"Azure AI Content Safety moderation failed: {str(e)}")
