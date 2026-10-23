import os
import requests
import json

def check_corpus_safety(text: str) -> dict:
    """
    Checks the safety of corpus text before embedding using Azure AI Content Safety.
    
    Args:
        text: The text string to check for safety.
        
    Returns:
        A dictionary containing the moderation results.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    
    data = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "blocklistNames": [],
        "breakdownByInput": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking corpus safety with Azure AI Content Safety: {e}")
        return {"error": str(e)}

