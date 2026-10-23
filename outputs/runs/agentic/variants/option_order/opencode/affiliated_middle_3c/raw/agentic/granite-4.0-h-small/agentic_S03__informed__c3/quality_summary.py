# [LATER-STEP] quality_summary.py

import os
from typing import List, Dict

# Provider identification: watsonx.ai guardrails / HAP detection via ibm-watsonx-ai SDK
# Example uses ibm-watsonx-ai library for content quality assessment
from ibm_watsonx_ai.nlp import WatsonxNlpServiceInstance
from ibm_watsonx_ai.auth import authenticate_service_credentials

# Load credentials from environment variables (or a local credentials file for demo)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
auth = authenticate_service_credentials(WATSONX_API_KEY, WATSONX_PROJECT_ID)
client = WatsonxNlpServiceInstance(auth=auth)


def summarize_quality(translations: List[str]) -> Dict[str, int]:
    """Summarize translation quality issues across a batch of translated strings.

    Uses Watsonx guardrails to detect toxicity, bias, hate speech, etc.
    Returns a simple count of flagged issues.

    Args:
        translations (List[str]): List of translated sentences.

    Returns:
        Dict[str, int]: Issue counts (e.g., {"toxic": 1, "bias": 0}).
    """
    issue_counts = {"toxic": 0, "bias": 0, "hate": 0, "unsafe": 0}
    for txt in translations:
        # Guardrails call returns a list of detected concerns
        concerns = client.content_moderation(text=txt, content_type="plain_text")
        # Example response format: [{"category": "toxic", "severity": "high"}, ...]
        for concern in concerns:
            category = concern.get("category", "other")
            if category in issue_counts:
                issue_counts[category] += 1
    return issue_counts


# Demo (guarded by __main__)
if __name__ == "__main__":
    sample_translations = ["This is great!", "You are stupid.", "I hate this product."]
    print("Quality summary:", summarize_quality(sample_translations))
