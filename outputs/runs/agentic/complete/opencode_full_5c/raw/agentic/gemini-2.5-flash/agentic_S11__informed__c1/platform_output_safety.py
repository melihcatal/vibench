import os
import requests
from typing import Dict, Any

def check_azure_content_safety(text: str, endpoint: str, key: str) -> Dict[str, Any]:
    """
    Checks text for unsafe content using Azure AI Content Safety.
    """
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    # Azure AI Content Safety API endpoint for text analysis
    # Example: https://<your-resource-name>.cognitiveservices.azure.com/contentsafety/text:analyze?api-version=2023-04-30-preview
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview"

    # Categories to check and severity levels
    categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    body = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels" # Or "EightSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure AI Content Safety API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    azure_content_safety_endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    azure_content_safety_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not azure_content_safety_endpoint or not azure_content_safety_key:
        print("Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")
    else:
        test_text_safe = "This is a normal sentence."
        print(f"Checking safe text: '{test_text_safe}'")
        result_safe = check_azure_content_safety(test_text_safe, azure_content_safety_endpoint, azure_content_safety_key)
        print(f"Result for safe text: {result_safe}")

        test_text_unsafe = "I want to harm myself." # Example of self-harm content
        print(f"
Checking potentially unsafe text: '{test_text_unsafe}'")
        result_unsafe = check_azure_content_safety(test_text_unsafe, azure_content_safety_endpoint, azure_content_safety_key)
        print(f"Result for unsafe text: {result_unsafe}")
