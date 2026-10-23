from safety_client import AzureContentSafetyClient
from safety_models import TextModerationRequest, TextModerationResponse
import os


def moderate_text(request: TextModerationRequest) -> TextModerationResponse:
    client = AzureContentSafetyClient()
    response_data = client.moderate_text(request.text)

    # Azure AI Content Safety response parsing
    categories = {
        "Hate": response_data["categories"]["Hate"],
        "Sexual": response_data["categories"]["Sexual"],
        "SelfHarm": response_data["categories"]["SelfHarm"],
        "Violence": response_data["categories"]["Violence"],
    }
    category_scores = {
        "Hate": response_data["category_scores"]["Hate"],
        "Sexual": response_data["category_scores"]["Sexual"],
        "SelfHarm": response_data["category_scores"]["SelfHarm"],
        "Violence": response_data["category_scores"]["Violence"],
    }

    suggested_action = "Accept"
    if any(categories.values()):
        suggested_action = "Reject"

    return TextModerationResponse(
        categories=categories,
        category_scores=category_scores,
        suggested_action=suggested_action,
        analyze_result=response_data,
    )
