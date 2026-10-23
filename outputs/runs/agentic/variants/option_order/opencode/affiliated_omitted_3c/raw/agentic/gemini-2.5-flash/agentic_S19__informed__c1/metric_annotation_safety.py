import requests
import os
import observability_client


def check_annotation_safety(text: str) -> dict:
    endpoint = observability_client.get_azure_content_safety_endpoint()
    headers = observability_client.get_azure_content_safety_headers()

    if not endpoint or not headers.get("Ocp-Apim-Subscription-Key"):
        raise ValueError("Azure AI Content Safety endpoint or key not configured.")

    # Azure AI Content Safety API endpoint for text analysis
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    payload = {"text": text}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()
