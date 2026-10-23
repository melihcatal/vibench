import os
import requests
import json
from security_models import ContentSafetyResult


def check_label_safety(text: str) -> ContentSafetyResult:
    """Checks secret labels and notes for unsafe text using Azure AI Content Safety.

    Args:
        text: The text to check for safety.

    Returns:
        A ContentSafetyResult object indicating if the text is safe and a reason if not.

    Raises:
        Exception: If Azure Content Safety endpoint or key is not set or API call fails.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    api_version = "2024-02-15-preview"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    data = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        # Analyze the results to determine safety
        for category in result.get("categoriesAnalysis", []):
            if (
                category["severity"] >= 2
            ):  # Assuming severity 2 or higher is considered unsafe
                return ContentSafetyResult(
                    is_safe=False,
                    reason=f"Unsafe content detected in category: {category['category']}",
                )

        return ContentSafetyResult(is_safe=True, reason="No unsafe content detected.")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Azure AI Content Safety API call failed: {e}")
    except json.JSONDecodeError:
        raise Exception("Failed to parse response from Azure AI Content Safety API.")
