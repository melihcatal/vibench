import os
import requests
import json

def check_ocr_safety(text: str) -> dict:
    """
    Checks extracted document text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    api_version = "2023-10-01"
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels"
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

    return response.json()

if __name__ == '__main__':
    # Example usage (requires environment variables set)
    # unsafe_text = "I hate you."
    # safety_analysis = check_ocr_safety(unsafe_text)
    # print(json.dumps(safety_analysis, indent=2))
    #
    # safe_text = "This is a normal document content."
    # safety_analysis = check_ocr_safety(safe_text)
    # print(json.dumps(safety_analysis, indent=2))
    pass
