import os
import requests
import json

def check_content_safety(text: str, endpoint: str = None, key: str = None) -> Dict[str, Any]:
    # Azure AI Content Safety API documentation:
    # https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-rest
    
    endpoint = endpoint or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = key or os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables or parameters must be set.")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
    return response.json()

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env vars)
    # endpoint_url = "YOUR_AZURE_CONTENT_SAFETY_ENDPOINT"
    # subscription_key = "YOUR_AZURE_CONTENT_SAFETY_KEY"
    # 
    # safe_text_analysis = check_content_safety("This is a perfectly safe sentence.", endpoint_url, subscription_key)
    # print(json.dumps(safe_text_analysis, indent=2))
    # 
    # unsafe_text_analysis = check_content_safety("I will kill you.", endpoint_url, subscription_key)
    # print(json.dumps(unsafe_text_analysis, indent=2))
    pass
