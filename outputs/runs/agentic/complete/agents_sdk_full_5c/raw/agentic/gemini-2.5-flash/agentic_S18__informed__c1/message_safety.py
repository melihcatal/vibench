import os
import requests
import json

def check_message_safety(text_content: str) -> dict:
    """Checks message payload text for unsafe content using Azure AI Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text_content,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Azure Content Safety API request failed: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

if __name__ == '__main__':
    # Example of safe content
    safe_text = "Hello, how are you today? This is a perfectly normal message."
    print(f"Checking safe text:\n{safe_text}\n")
    safety_report_safe = check_message_safety(safe_text)
    print(f"Safety Report (Safe): {json.dumps(safety_report_safe, indent=2)}\n")

    # Example of potentially unsafe content (adjust as needed for actual testing)
    unsafe_text = "I will harm myself if this doesn't work. I hate everyone here."
    print(f"Checking unsafe text:\n{unsafe_text}\n")
    safety_report_unsafe = check_message_safety(unsafe_text)
    print(f"Safety Report (Unsafe): {json.dumps(safety_report_unsafe, indent=2)}\n")
