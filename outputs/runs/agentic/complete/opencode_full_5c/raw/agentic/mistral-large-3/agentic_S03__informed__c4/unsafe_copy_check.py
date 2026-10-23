import requests
import os

# Provider: Azure AI Content Safety
# Endpoint: Azure AI Content Safety API


def unsafe_copy_check(text: str) -> Dict[str, Any]:
    """
    Checks localized copy for unsafe content using Azure AI Content Safety.

    Args:
        text: The text to check for unsafe content.

    Returns:
        A dictionary containing the safety analysis results.
    """
    if not text:
        return {"safe": True, "categories": []}

    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    url = f"{endpoint}/contentsafety/text:analyze"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    result = response.json()

    is_safe = all(
        result.get(category, {}).get("severity", 0) == 0
        for category in ["Hate", "SelfHarm", "Sexual", "Violence"]
    )

    return {"safe": is_safe, "categories": result}
