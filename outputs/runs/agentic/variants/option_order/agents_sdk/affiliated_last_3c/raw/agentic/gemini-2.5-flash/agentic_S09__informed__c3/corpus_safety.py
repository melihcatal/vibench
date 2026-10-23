import os
import requests
from dotenv import load_dotenv

load_dotenv() # Load environment variables

def check_corpus_safety(text: str) -> dict:
    """
    Checks the safety of the given text using Azure AI Content Safety.
    
    Args:
        text: The text content to check.
        
    Returns:
        A dictionary containing the safety analysis results from Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables not set.")

    api_version = "2023-04-30-preview" # Specific API version for Azure AI Content Safety
    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"
    
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    
    data = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety with Azure AI Content Safety: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY)
    # text_to_check_safe = "This is a perfectly safe and delightful piece of text about happy puppies."
    # text_to_check_unsafe = "I hate this, I want to hurt someone."
    
    # print("Checking safe text:")
    # result_safe = check_corpus_safety(text_to_check_safe)
    # print(result_safe)
    
    # print("\nChecking unsafe text:")
    # result_unsafe = check_corpus_safety(text_to_check_unsafe)
    # print(result_unsafe)
    pass
