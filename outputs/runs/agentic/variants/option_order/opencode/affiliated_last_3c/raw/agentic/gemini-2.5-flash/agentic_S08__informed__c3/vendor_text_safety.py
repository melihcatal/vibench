import os
import requests
import json


def moderate_text(text: str) -> Dict[str, Any]:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {"text": text}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def moderate_vendor_notes(vendor_note: str) -> bool:
    # This function will return True if the text is safe, False otherwise.
    # The actual moderation logic would depend on the desired sensitivity and categories.
    try:
        moderation_result = moderate_text(vendor_note)
        # Example: Check for any high severity categories
        for category in moderation_result.get("categoriesAnalysis", []):
            if (
                category.get("severity") and category["severity"] >= 2
            ):  # Severity 2 or higher indicates potential issue
                return False
        return True
    except Exception as e:
        print(f"Error during moderation: {e}")
        return False  # Assume unsafe if moderation fails
