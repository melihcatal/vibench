import os
import requests
import json

def check_text_safety(text_content: str):
    """
    Checks user-generated text fields for unsafe content using
    Azure AI Content Safety.

    :param text_content: The text to analyze.
    :return: The JSON response from the Azure AI Content Safety API.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    # API version is required in the URL
    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }

    payload = {
        "text": text_content,
        # Define severity levels to detect for each category
        "hateSeverity": 1,
        "selfHarmSeverity": 1,
        "sexualSeverity": 1,
        "violenceSeverity": 1,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while calling the Azure AI Content Safety API: {e}")
        raise
