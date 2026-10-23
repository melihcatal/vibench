import os
from typing import Dict, Any, Optional
from googleapiclient import discovery
from google.cloud import language_v1


def get_safety_client() -> discovery.Resource:
    """
    Initializes and returns a Google Cloud Content Moderation API client.
    """
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.getenv("GOOGLE_API_KEY"),
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )


def get_nlp_client() -> language_v1.LanguageServiceClient:
    """
    Initializes and returns a Google Cloud Natural Language API client.
    """
    return language_v1.LanguageServiceClient()


def get_safety_settings(category_thresholds: Dict[str, str]) -> Dict[str, Any]:
    """
    Converts category thresholds into Google Cloud Content Moderation API format.
    """
    return {
        category: {"scoreThreshold": threshold}
        for category, threshold in category_thresholds.items()
    }


def get_redaction_config() -> Dict[str, Any]:
    """
    Returns default redaction configuration for unsafe spans.
    """
    return {
        "sentiment_threshold": -0.5,
        "redaction_placeholder": "[REDACTED]",
    }
