import os
import requests


def log_text_safety(text: str) -> Dict[str, Any]:
    """Check selected log message text for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    url = f"{endpoint}/contentsafety/text:analyze"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to check log text safety using Azure AI Content Safety: {e}")
        raise
