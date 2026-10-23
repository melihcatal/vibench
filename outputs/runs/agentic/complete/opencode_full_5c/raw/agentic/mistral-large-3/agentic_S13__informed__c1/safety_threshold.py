from typing import Dict, Any

from safety_client import get_content_safety_client
from safety_models import ModerationRequest, ModerationResponse, normalize_response


def apply_safety_threshold(
    text: str, thresholds: Dict[str, int] = None, context: Dict[str, Any] = None
) -> bool:
    """
    Applies category thresholds to decide whether to allow text using Azure AI Content Safety.
    Default thresholds: Hate=2, Sexual=2, Violence=2, SelfHarm=2, Harassment=2.
    """
    client = get_content_safety_client()
    thresholds = thresholds or {
        "Hate": 2,
        "Sexual": 2,
        "Violence": 2,
        "SelfHarm": 2,
        "Harassment": 2,
    }

    request = ModerationRequest(
        text=text, categories=list(thresholds.keys()), context=context or {}
    )

    try:
        response = client.analyze_text(
            text=text, categories=request.categories, output_type="FourSeverityLevels"
        )
        normalized_response = normalize_response(response)

        for category, score in normalized_response.category_scores.items():
            if score > thresholds.get(category, 2):
                return False
        return True
    except Exception as e:
        raise Exception(f"Azure AI Content Safety threshold check failed: {str(e)}")
