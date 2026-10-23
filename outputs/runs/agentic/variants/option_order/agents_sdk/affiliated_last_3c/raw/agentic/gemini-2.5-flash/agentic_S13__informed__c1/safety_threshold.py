import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def safety_threshold(text: str, category_thresholds: dict = None) -> dict:
    """
    Applies category thresholds to decide whether to allow text based on Azure AI Content Safety scores.
    """
    if category_thresholds is None:
        category_thresholds = {
            "hate": 2,  # Example: block if hate severity is 2 or higher
            "self_harm": 2,
            "sexual": 2,
            "violence": 2
        }

    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE
        ]
    )

    response = client.analyze_text(request)

    decision = {
        "text": text,
        "allowed": True,
        "reasons": [],
        "category_decisions": {}
    }

    for category_result in response.categories_analysis:
        category_name = category_result.category.value.lower()
        severity = category_result.severity
        threshold = category_thresholds.get(category_name, 999) # Default to a high threshold if not specified

        is_blocked_by_category = severity >= threshold

        decision["category_decisions"][category_name] = {
            "severity": severity,
            "threshold": threshold,
            "blocked": is_blocked_by_category
        }

        if is_blocked_by_category:
            decision["allowed"] = False
            decision["reasons"].append(f"Blocked by {category_name} (severity {severity} >= threshold {threshold})")

    return decision

if __name__ == '__main__':
    # Example usage - ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set
    # text1 = "I love this product, it's amazing."
    # text2 = "I will hurt someone."
    # text3 = "You are so ugly."

    # print(safety_threshold(text1))
    # print(safety_threshold(text2))
    # print(safety_threshold(text3, category_thresholds={"hate": 1, "violence": 3}))
    pass
