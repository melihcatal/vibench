import os
import requests
import json

def check_script_safety(text: str, endpoint: str, key: str) -> dict:
    """Checks text for unsafe content using Azure AI Content Safety."""
    # Azure AI Content Safety API details
    # https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-rest
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
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        print("Azure AI Content Safety analysis result:")
        print(json.dumps(result, indent=2))
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure AI Content Safety: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are set.
    # Example usage:
    # text_to_check = "I will hurt you."
    # endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    # key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    # if endpoint and key:
    #     safety_report = check_script_safety(text_to_check, endpoint, key)
    # else:
    #     print("Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")
    pass
