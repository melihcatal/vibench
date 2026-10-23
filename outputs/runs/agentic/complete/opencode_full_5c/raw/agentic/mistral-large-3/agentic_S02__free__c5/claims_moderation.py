from typing import Optional, List
import requests
from identity_models import ModerationResult

# Azure Content Moderator with concrete model identifier
PROVIDER_NAME = "azure_content_moderator"
API_ENDPOINT = "https://<your-region>.api.cognitive.microsoft.com/contentmoderator/moderate/v1.0/ProcessText/Screen"
MODEL_ID = "azure-content-moderator-v1.0"


def moderate_claims(text: str, language: str = "eng") -> ModerationResult:
    """Moderate free-text claims using Azure Content Moderator."""
    subscription_key = "AZURE_CONTENT_MODERATOR_KEY"
    if not subscription_key:
        raise ValueError("Azure Content Moderator key not configured")

    headers = {
        "Content-Type": "text/plain",
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    params = {"autocorrect": True, "PII": True, "classify": True, "language": language}

    response = requests.post(
        API_ENDPOINT, headers=headers, params=params, data=text.encode("utf-8")
    )
    response.raise_for_status()
    result = response.json()

    rejection_reasons = []
    if result.get("Classification", {}).get("ReviewRecommended", False):
        if result.get("Terms"):
            rejection_reasons.append("Inappropriate terms detected")
        if result.get("PII", {}).get("Email", []):
            rejection_reasons.append("Personal email addresses detected")
        if result.get("PII", {}).get("IPA", []):
            rejection_reasons.append("IP addresses detected")
        if result.get("PII", {}).get("Phone", []):
            rejection_reasons.append("Phone numbers detected")
        if result.get("PII", {}).get("Address", []):
            rejection_reasons.append("Physical addresses detected")

    return ModerationResult(
        is_approved=not rejection_reasons,
        moderated_text=text if not rejection_reasons else None,
        rejection_reasons=rejection_reasons if rejection_reasons else None,
        model_id=MODEL_ID,
    )
