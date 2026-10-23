import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextCategory


def apply_category_thresholds(text: str, thresholds: dict):
    """
    Applies category thresholds to decide whether to allow text using Azure AI Content Safety analysis.
    The thresholds dictionary should contain category names as keys and a minimum severity (1-4) as values.
    E.g., {"Hate": 2, "Sexual": 3}
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = {
        "text": text,
        "categories": [
            TextCategory.VIOLENCE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.HATE,
        ],
        "outputType": "FourSeverityLevels",
    }
    response = client.analyze_text(request)
    analysis = response.to_dict()

    allowed = True
    reasons = []

    for category_analysis in analysis.get("categoriesAnalysis", []):
        category = category_analysis.get("category")
        severity = category_analysis.get("severity")
        if category and severity is not None and category in thresholds:
            if severity >= thresholds[category]:
                allowed = False
                reasons.append(
                    f"Text exceeded threshold for category '{category}' with severity {severity} (threshold {thresholds[category]})"
                )

    return {"allowed": allowed, "reasons": reasons, "analysis": analysis}
