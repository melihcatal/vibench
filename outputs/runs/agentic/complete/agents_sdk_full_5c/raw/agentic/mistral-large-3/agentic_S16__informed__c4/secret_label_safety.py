import requests
import os


def check_secret_labels_for_unsafe_text(text: str) -> dict:
    """
    Check secret labels and notes for unsafe text using Azure AI Content Safety.
    
    Args:
        text: The text to analyze.
    
    Returns:
        A dictionary containing safety analysis results.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    
    url = f"{endpoint}/contentsafety/text:analyze"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    
    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "breakByBlock": False,
    }
    
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()