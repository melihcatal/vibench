from model_client import get_perspective_client
from model_models import SafetyRating


def platform_output_safety(text: str) -> SafetyRating:
    """
    Checks platform model output for unsafe content using Google's Perspective API.
    """
    client = get_perspective_client()

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    toxicity_score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

    is_safe = toxicity_score < 0.7

    scores = {"toxicity": toxicity_score}

    return SafetyRating(is_safe=is_safe, scores=scores)
