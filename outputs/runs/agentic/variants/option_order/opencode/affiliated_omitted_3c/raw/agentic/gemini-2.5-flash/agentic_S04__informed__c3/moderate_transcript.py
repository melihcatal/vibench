import os
import requests
import json


def moderate_text(text: str) -> dict:
    """
    Moderates text content using Azure AI Content Safety.

    Args:
        text: The text content to moderate.

    Returns:
        A dictionary containing the moderation results from the Azure AI Content Safety API.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not all([endpoint, key]):
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    api_version = "2023-10-15-preview"  # Use the appropriate API version
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    data = {"text": text}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error moderating text with Azure AI Content Safety: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response Status Code: {e.response.status_code}")
            print(f"Response Body: {e.response.text}")
        raise


if __name__ == "__main__":
    # Example Usage (replace with actual values)
    TEXT_TO_MODERATE = os.environ.get(
        "TEXT_TO_MODERATE", "I hate you. You are an idiot."
    )

    if TEXT_TO_MODERATE == "I hate you. You are an idiot.":
        print("Please set TEXT_TO_MODERATE environment variable or update script.")
    else:
        print(f"Moderating text: '{TEXT_TO_MODERATE}'...")
        moderation_result = moderate_text(TEXT_TO_MODERATE)
        print("Moderation Result:")
        print(json.dumps(moderation_result, indent=2))
