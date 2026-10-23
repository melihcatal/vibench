import os
import requests
import json

def moderate_profile_text(text):
    """
    Moderates profile text using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        return {"error": "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."}

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourSeverityLevels"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage
    profile_bio_good = "Hello, I am a new user, excited to explore!"
    profile_bio_bad = "I hate everyone, this service is terrible." # Example of potentially harmful content

    print("Moderating good profile text:")
    result_good = moderate_profile_text(profile_bio_good)
    print(result_good)

    print("\nModerating bad profile text:")
    result_bad = moderate_profile_text(profile_bio_bad)
    print(result_bad)
