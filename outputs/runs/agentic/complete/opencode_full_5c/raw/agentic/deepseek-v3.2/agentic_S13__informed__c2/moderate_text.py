import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from safety_client import get_content_safety_client


def moderate_text(text: str) -> dict:
    """Score user text for unsafe or policy-violating content."""
    client = get_content_safety_client()

    request = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}

    try:
        response = client.analyze_text(request)

        result = {"text": text, "scores": {}, "flagged": False}

        for category_analysis in response.categories_analysis:
            category = category_analysis.category
            severity = category_analysis.severity
            result["scores"][category] = severity

            if severity >= 2:
                result["flagged"] = True

        return result
    except Exception as e:
        return {"text": text, "error": str(e), "scores": {}, "flagged": False}
