import os
import requests
from model_models import SafetyCheckResult


def check_platform_output_safety(text: str) -> SafetyCheckResult:
    """Checks platform model output for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        is_safe = True
        categories_result = {}
        for category in result.get("categoriesAnalysis", []):
            severity = category.get("severity", 0)
            categories_result[category.get("category")] = {"severity": severity}
            if severity > 0:
                is_safe = False

        return SafetyCheckResult(is_safe=is_safe, categories=categories_result)

    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure AI Content Safety: {e}")
        # Depending on the desired behavior, you might want to re-raise or return a default/error result
        return SafetyCheckResult(is_safe=False, categories={"error": str(e)})
