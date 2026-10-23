import os
import requests
import json

def check_secret_text_safety(text: str) -> dict:
    """Checks secret labels and notes for unsafe text using Azure AI Content Safety.

    Args:
        text (str): The text content (e.g., secret labels, notes, descriptions) to check.

    Returns:
        dict: A dictionary containing the safety analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {"text": text}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Error connecting to Azure AI Content Safety: {e}")
    except json.JSONDecodeError:
        raise ValueError("Received non-JSON response from Azure AI Content Safety.")

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY env vars)
    # unsafe_text = "This secret contains a very bad word and potentially harmful instructions."
    # safety_report = check_secret_text_safety(unsafe_text)
    # print(json.dumps(safety_report, indent=2))

    # safe_text = "This is a benign secret label for a test environment."
    # safety_report_safe = check_secret_text_safety(safe_text)
    # print(json.dumps(safety_report_safe, indent=2))
    pass
