import os
import requests
import json

def check_platform_output_safety(text: str) -> dict:
    """Checks platform model output for unsafe content using Azure AI Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    api_version = "2023-10-15-preview"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence"
        ],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Set these environment variables before running
    # export AZURE_CONTENT_SAFETY_ENDPOINT="https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/"
    # export AZURE_CONTENT_SAFETY_KEY="YOUR_API_KEY"
    
    test_text_safe = "The quick brown fox jumps over the lazy dog."
    test_text_unsafe = "I will harm you."

    print("Checking safe text:")
    result_safe = check_platform_output_safety(test_text_safe)
    print(json.dumps(result_safe, indent=2))

    print("\nChecking unsafe text:")
    result_unsafe = check_platform_output_safety(test_text_unsafe)
    print(json.dumps(result_unsafe, indent=2))
