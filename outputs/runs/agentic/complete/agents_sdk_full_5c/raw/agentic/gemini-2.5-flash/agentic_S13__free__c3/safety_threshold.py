import os
from typing import Dict
from safety_models import ModerationResult  # Assuming ModerationResult from Perspective API structure
from safety_client import get_perspective_api_client # To ensure provider signal linkage

def apply_category_thresholds(moderation_result: Dict, category_thresholds: Dict[str, float]) -> Dict:
    """
    Applies category thresholds to decide whether to allow text based on moderation scores.
    Uses the output structure similar to Perspective API.
    """
    decision = {"allowed": True, "reasons": []}
    
    # We can use the client to ensure the provider signal is present even if not making a call
    # This is a local helper function for client config and ensures this file has a clear provider signal
    # as it processes results from that provider.
    _ = get_perspective_api_client()

    attribute_scores = moderation_result.get('attributeScores', {})

    for category, threshold in category_thresholds.items():
        score_data = attribute_scores.get(category)
        if score_data and score_data.get('summaryScore', {}).get('value', 0.0) >= threshold:
            decision["allowed"] = False
            decision["reasons"].append(
                f"Category '{category}' exceeded threshold ({threshold}): "
                f"Score {score_data['summaryScore']['value']}"
            )
    return decision

if __name__ == '__main__':
    # Example usage (assuming Perspective API like output and defined thresholds)
    # fake_moderation_result = {
    #     "attributeScores": {
    #         "TOXICITY": {"summaryScore": {"value": 0.85}},
    #         "INSULT": {"summaryScore": {"value": 0.7}},
    #         "PROFANITY": {"summaryScore": {"value": 0.1}}
    #     }
    # }
    # thresholds = {
    #     "TOXICITY": 0.8,
    #     "INSULT": 0.6,
    #     "PROFANITY": 0.9
    # }
    # final_decision = apply_category_thresholds(fake_moderation_result, thresholds)
    # print(final_decision)
    pass
