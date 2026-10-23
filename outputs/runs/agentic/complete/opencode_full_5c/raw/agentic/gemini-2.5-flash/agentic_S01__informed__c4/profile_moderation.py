import os
import requests
import json


def profile_moderation(profile_text: str) -> dict:
    """Moderates profile text before account activation using Azure AI Content Safety.

    Args:
        profile_text: The text content of the user's profile.

    Returns:
        A dictionary containing moderation results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY environment variable not set."
        )

    api_version = "2023-10-01-preview"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    # Example request body for text analysis
    # Customize the categories and severity if needed
    body = {
        "text": profile_text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],  # Optional: specify blocklists if configured
        "outputType": "FourCategories",
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Azure AI Content Safety moderation failed: {e}")
