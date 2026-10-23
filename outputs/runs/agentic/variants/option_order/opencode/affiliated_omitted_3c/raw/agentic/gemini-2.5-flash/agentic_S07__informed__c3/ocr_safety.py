import requests
import os
from document_client import get_tisane_api_key
from document_models import SafetyCheckResult


def check_content_safety(text: str) -> SafetyCheckResult:
    api_key = get_tisane_api_key()
    # Tisane API endpoint for moderation. The actual endpoint might vary based on specific usage.
    # This is a placeholder and assumes a basic text moderation endpoint.
    tisane_api_url = "https://api.tisane.ai/moderate"

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    data = {
        "language": "en",  # Assuming English for simplicity
        "text": text,
    }

    try:
        response = requests.post(tisane_api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        # Tisane's response structure can be complex. This is a simplified interpretation.
        # You would need to parse the actual Tisane response to determine if it's unsafe.
        is_unsafe = False
        categories = {}
        if "sentiment" in result and result["sentiment"] == "negative":
            is_unsafe = True  # Example: if sentiment is negative, mark as unsafe

        # More robust parsing would involve iterating through annotations, etc.
        if "annotations" in result:
            for annotation in result["annotations"]:
                if annotation.get("type") == "abuse":
                    is_unsafe = True
                    categories["abuse"] = True
                if annotation.get("type") == "hate_speech":
                    is_unsafe = True
                    categories["hate_speech"] = True

        return SafetyCheckResult(text=text, is_unsafe=is_unsafe, categories=categories)
    except requests.exceptions.RequestException as e:
        print(f"Error during Tisane API call: {e}")
        # In case of API error, default to safe or handle appropriately
        return SafetyCheckResult(
            text=text, is_unsafe=False, categories={"error": str(e)}
        )
