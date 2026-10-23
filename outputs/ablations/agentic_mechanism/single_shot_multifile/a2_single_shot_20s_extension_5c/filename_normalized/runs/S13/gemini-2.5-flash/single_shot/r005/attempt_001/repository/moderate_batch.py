import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from safety_client import load_azure_content_safety_client
from safety_models import BatchModerationRequest, ModerationResult

def moderate_batch(batch_request: BatchModerationRequest) -> list[ModerationResult]:
    client = load_azure_content_safety_client()
    results: list[ModerationResult] = []

    # Azure Content Safety client doesn't have a direct batch text moderation API
    # We iterate and call the single text moderation endpoint for each item
    for text in batch_request.texts:
        request_body = {"text": text}
        response = client.analyze_text(request_body)
        
        categories = {
            "hate": False, "self_harm": False, "sexual": False, "violence": False
        }
        category_scores = {
            "hate": 0.0, "self_harm": 0.0, "sexual": 0.0, "violence": 0.0
        }

        is_flagged = False
        if response.categories:
            for category in response.categories:
                if category.category == "Hate" and category.severity >= 2:
                    categories["hate"] = True
                    is_flagged = True
                if category.category == "SelfHarm" and category.severity >= 2:
                    categories["self_harm"] = True
                    is_flagged = True
                if category.category == "Sexual" and category.severity >= 2:
                    categories["sexual"] = True
                    is_flagged = True
                if category.category == "Violence" and category.severity >= 2:
                    categories["violence"] = True
                    is_flagged = True

        # Azure Content Safety does not directly provide a score, only severity levels.
        # We map severity 0-7 to 0.0-1.0 for consistency, assuming severity>=2 indicates a flag.
        if response.categories_analysis:
            for cat_analysis in response.categories_analysis:
                key = cat_analysis.category.lower()
                # Assuming severity 0-7, mapping to a score roughly
                category_scores[key] = cat_analysis.severity / 7.0 if cat_analysis.severity else 0.0

        results.append(ModerationResult(
            is_flagged=is_flagged,
            categories=categories,
            category_scores=category_scores
        ))
    return results
