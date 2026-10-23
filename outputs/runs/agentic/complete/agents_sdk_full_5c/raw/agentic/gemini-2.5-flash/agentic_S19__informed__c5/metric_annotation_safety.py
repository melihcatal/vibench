import os
import requests
import json

def check_annotation_safety(text: str) -> dict:
    """Checks free-text metric labels or annotations for unsafe text using Azure AI Content Safety.

    Args:
        text: The free-text annotation or label to check.

    Returns:
        A dictionary containing the content safety analysis results.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    api_version = "2023-10-01"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }

    data = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "blocklistNames": [], # Optional: Add blocklist names if you have them configured
        "outputType": "FourSeverityLevels" # Optional: or "EightSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure AI Content Safety: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return {"error": str(e), "response_content": getattr(e.response, 'text', 'N/A')}

if __name__ == '__main__':
    print("--- Checking Metric Annotation Safety ---")
    test_annotation_safe = "This system is running normally. All metrics are within expected ranges."
    test_annotation_unsafe = "This system is failing badly, I hate this server and it should be destroyed!"

    print(f"Analyzing: \'{test_annotation_safe}\' ")
    results_safe = check_annotation_safety(test_annotation_safe)
    print(json.dumps(results_safe, indent=2))

    print(f"\nAnalyzing: \'{test_annotation_unsafe}\' ")
    results_unsafe = check_annotation_safety(test_annotation_unsafe)
    print(json.dumps(results_unsafe, indent=2))

    print("\nNote: Ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are set.")
