import requests
import os
import json

def check_script_safety_azure_ai_content_safety(text: str):
    """
    Checks narration scripts for unsafe content using Azure AI Content Safety.
    Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")

    api_version = "2023-10-01" # Or latest supported version
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    body = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()
        print("Azure AI Content Safety Analysis Result:")
        print(json.dumps(result, indent=2))
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure AI Content Safety API: {e}")
        return None

if __name__ == "__main__":
    # Example usage (ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set)
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com/"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_CONTENT_SAFETY_KEY"

    # script_to_check = "This script contains some potentially offensive language."
    # print(f"Checking script: '{script_to_check}'")
    # safety_result = check_script_safety_azure_ai_content_safety(script_to_check)

    # script_to_check_safe = "This is a completely safe script about happy puppies."
    # print(f"Checking script: '{script_to_check_safe}'")
    # safety_result_safe = check_script_safety_azure_ai_content_safety(script_to_check_safe)

    # For demonstration purposes, without actual keys:
    print("To run this example, please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.")
    print("Checking a dummy script:")
    check_script_safety_azure_ai_content_safety("Hello, world! This is a test for content safety.")
