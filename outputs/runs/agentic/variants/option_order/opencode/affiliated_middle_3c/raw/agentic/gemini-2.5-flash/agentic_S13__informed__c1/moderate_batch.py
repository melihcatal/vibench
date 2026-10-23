from safety_client import AzureContentSafetyClient
from safety_models import (
    BatchModerationRequest,
    BatchModerationResponse,
    TextModerationResponse,
)
import os


def moderate_batch(request: BatchModerationRequest) -> BatchModerationResponse:
    client = AzureContentSafetyClient()
    batch_results_data = client.moderate_batch(request.texts)

    moderation_responses = []
    for response_data in batch_results_data:
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

        moderation_responses.append(
            TextModerationResponse(
                categories=categories,
                category_scores=category_scores,
                suggested_action=suggested_action,
                analyze_result=response_data,
            )
        )

    return BatchModerationResponse(results=moderation_responses)
