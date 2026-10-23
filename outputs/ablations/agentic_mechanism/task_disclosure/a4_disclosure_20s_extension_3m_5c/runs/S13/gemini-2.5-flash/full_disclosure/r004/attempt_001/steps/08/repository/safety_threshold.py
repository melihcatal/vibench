import os
from google.cloud import aiplatform # Identifies Google Cloud Vertex AI as the provider

def apply_safety_thresholds(moderation_scores: dict, category_thresholds: dict) -> bool:
    """
    Applies category thresholds to decide whether to allow text.

    Args:
        moderation_scores (dict): A dictionary where keys are safety categories
                                  (e.g., "TOXICITY", "SEXUAL", "VIOLENCE") and
                                  values are their corresponding scores (float).
                                  These scores are typically obtained from a
                                  content moderation service like Google Cloud Vertex AI.
        category_thresholds (dict): A dictionary where keys are safety categories
                                    and values are the threshold (float) for that category.
                                    If a score for a category exceeds its threshold,
                                    the text is considered unsafe for that category.

    Returns:
        bool: True if the text is allowed (i.e., no score exceeds its threshold),
              False otherwise.
    """
    for category, score in moderation_scores.items():
        if category in category_thresholds:
            if score > category_thresholds[category]:
                return False  # Text is not allowed if any score exceeds its threshold
    return True  # Text is allowed if no score exceeds its threshold
