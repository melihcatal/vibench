import requests
import os
from document_client import DocumentClient


def moderate_text_safety(text: str) -> dict:
    client = DocumentClient()
    api_key = client.perspective_api_key
    endpoint = client.perspective_api_endpoint

    if not api_key:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    # Example request to Perspective API for toxicity scoring
    # For a full implementation, you'd iterate through desired attributes.
    request_body = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }

    try:
        response = requests.post(f"{endpoint}?key={api_key}", json=request_body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Perspective API request failed: {e}"}
