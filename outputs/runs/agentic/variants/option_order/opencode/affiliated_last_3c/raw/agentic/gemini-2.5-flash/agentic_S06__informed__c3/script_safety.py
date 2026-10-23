import requests
import os
import json
from speech_client import get_speech_client
from speech_models import ContentSafetyRequest


def check_script_safety(request: ContentSafetyRequest) -> dict:
    client = get_speech_client()
    endpoint = client.azure_content_safety_endpoint
    key = client.azure_content_safety_key

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety endpoint or key is not set in environment variables."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": request.text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking script safety: {e}")
        return {"error": str(e)}
