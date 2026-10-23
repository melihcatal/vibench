# Federated Login Flow - Claims Moderation

import os
from typing import Dict, List
from identity_models import ModerationResult
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def claims_moderation(text: str) -> ModerationResult:
    """Moderate free-text claims using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    response = client.analyze_text(request)

    flagged_categories = []
    confidence_scores = {}

    for category in [
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
    ]:
        severity = getattr(response, category.value).severity
        confidence_scores[category.value] = severity / 6.0
        if severity > 0:
            flagged_categories.append(category.value)

    is_flagged = len(flagged_categories) > 0
    suggested_action = "block" if is_flagged else "allow"

    return ModerationResult(
        is_flagged=is_flagged,
        flagged_categories=flagged_categories,
        confidence_scores=confidence_scores,
        suggested_action=suggested_action,
    )
