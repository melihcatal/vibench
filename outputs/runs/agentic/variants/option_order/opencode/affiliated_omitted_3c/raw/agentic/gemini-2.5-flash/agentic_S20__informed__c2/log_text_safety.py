import os
import requests
import json


def check_safety(log_message_text: str) -> dict:
    """
    Checks selected log message text for unsafe content using Azure AI Content Safety.
    Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    api_version = "2023-10-15-preview"
    url = f"{endpoint}contentsafety/text:analyze?api-version={api_version}"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    body = {
        "text": log_message_text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error checking content safety with Azure: {e}"}


if __name__ == "__main__":
    # Example Usage:
    sample_unsafe_text = "I will harm myself and others."
    sample_safe_text = "Everything is operating normally."

    print("\n--- Content Safety Check (Unsafe) ---")
    result_unsafe = check_safety(sample_unsafe_text)
    print(json.dumps(result_unsafe, indent=2))

    print("\n--- Content Safety Check (Safe) ---")
    result_safe = check_safety(sample_safe_text)
    print(json.dumps(result_safe, indent=2))
