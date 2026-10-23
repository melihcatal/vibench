import os
import requests
import json

def check_content_safety(text_to_check: str) -> dict | None:
    """
    Checks text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        print("AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY environment variables not set.")
        return None

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }
    body = {
        "text": text_to_check,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure AI Content Safety API: {e}")
        return None
    except json.JSONDecodeError:
        print("Failed to decode JSON response from Azure AI Content Safety API.")
        return None
