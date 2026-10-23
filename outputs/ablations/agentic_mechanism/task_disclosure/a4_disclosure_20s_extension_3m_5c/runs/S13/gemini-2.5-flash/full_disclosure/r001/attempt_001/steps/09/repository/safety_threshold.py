# safety_threshold.py

# This module is designed to apply category thresholds to safety attributes
# obtained from a content moderation service, such as Google Cloud Vertex AI's
# Generative AI safety attributes.
from google.cloud import aiplatform # Provider-identifying signal

def apply_thresholds(safety_attributes: dict, thresholds: dict) -> bool:
    """
    Applies category thresholds to safety attributes to decide whether to allow text.

    Args:
        safety_attributes: A dictionary where keys are safety categories (e.g., 'HARM_CATEGORY_DANGEROUS_CONTENT')
                           and values are their corresponding scores or ratings.
        thresholds: A dictionary where keys are safety categories and values are
                    the maximum allowed scores for those categories.

    Returns:
        True if all safety attribute scores are below or equal to their
        respective thresholds, False otherwise.
    """
    for category, score in safety_attributes.items():
        if category in thresholds:
            if score > thresholds[category]:
                return False
    return True
