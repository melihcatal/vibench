import os
import requests
import json

def check_corpus_safety(text: str, endpoint: str = None, key: str = None) -> dict:
    """
    Checks the safety of a given text using Azure AI Content Safety.
    
    Args:
        text: The text content to check.
        endpoint: The endpoint URL for the Azure Content Safety service.
        key: The subscription key for the Azure Content Safety service.
    
    Returns:
        A dictionary containing the safety analysis results.
    """
    if not endpoint:
        endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    if not key:
        key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be provided or set as environment variables.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables)
    
    # Example of a potentially unsafe text
    unsafe_text = "I hate this! I will hurt myself." 
    
    # Example of a safe text
    safe_text = "The weather is nice today, let's go for a walk."

    print("Checking unsafe text:")
    result_unsafe = check_corpus_safety(unsafe_text)
    print(json.dumps(result_unsafe, indent=2))

    print("
Checking safe text:")
    result_safe = check_corpus_safety(safe_text)
    print(json.dumps(result_safe, indent=2))
