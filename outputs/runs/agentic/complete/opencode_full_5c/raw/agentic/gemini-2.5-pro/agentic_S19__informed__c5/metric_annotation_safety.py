import os
import requests
import json


def check_annotation_safety(text: str) -> dict:
    """
    Checks free-text for safety using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "Azure Content Safety credentials are not set in environment variables."
        )

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "status_code": e.response.status_code if e.response else None,
        }


if __name__ == "__main__":
    # Example safe text
    safe_text_result = check_annotation_safety("This is a normal metric annotation.")
    print("Safe text analysis:")
    print(json.dumps(safe_text_result, indent=2))

    # Example unsafe text
    unsafe_text_result = check_annotation_safety(
        "This is a hateful and violent comment."
    )
    print("\nUnsafe text analysis:")
    print(json.dumps(unsafe_text_result, indent=2))
