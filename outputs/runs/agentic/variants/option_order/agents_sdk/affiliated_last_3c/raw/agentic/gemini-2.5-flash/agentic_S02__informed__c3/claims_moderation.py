import os
import requests
import json
from identity_models import ModerationResult

def moderate_text_claim(text_claim: str) -> ModerationResult:
    """
    Moderates a given text claim using Azure AI Content Safety.

    Args:
        text_claim: The free-text claim or note to moderate.

    Returns:
        A ModerationResult object indicating if the text was flagged and why.
    """
    AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not all([AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY]):
        raise ValueError("Missing AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY environment variables.")

    # Azure AI Content Safety API specific URL
    api_version = "2023-10-01-preview" # Use a specific API version
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text_claim,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "blocklistNames": [],
        "outputType": "FourHundered"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status() # Raise an exception for HTTP errors

    result = response.json()

    is_flagged = False
    reasons = []
    for category_analysis in result.get("categoriesAnalysis", []):
        if category_analysis.get("severity") is not None and category_analysis["severity"] > 0:
            is_flagged = True
            reasons.append(f"{category_analysis["category"]} (severity: {category_analysis["severity"]})")

    return ModerationResult(
        is_flagged=is_flagged,
        reasons=reasons,
        raw_response=result
    )

if __name__ == "__main__":
    # Example usage
    os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/"
    os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_AZURE_CONTENT_SAFETY_KEY"

    test_claim_safe = "This is a perfectly fine note about my preferences."
    test_claim_unsafe = "I hate everyone and want to hurt myself."
    test_claim_violence = "I will assault anyone who gets in my way."

    try:
        print(f"\nModerating: \"{test_claim_safe}\" ")
        result_safe = moderate_text_claim(test_claim_safe)
        print(f"  Flagged: {result_safe.is_flagged}, Reasons: {result_safe.reasons}")

        print(f"\nModerating: \"{test_claim_unsafe}\" ")
        result_unsafe = moderate_text_claim(test_claim_unsafe)
        print(f"  Flagged: {result_unsafe.is_flagged}, Reasons: {result_unsafe.reasons}")

        print(f"\nModerating: \"{test_claim_violence}\" ")
        result_violence = moderate_text_claim(test_claim_violence)
        print(f"  Flagged: {result_violence.is_flagged}, Reasons: {result_violence.reasons}")

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"Error during moderation: {e}")
