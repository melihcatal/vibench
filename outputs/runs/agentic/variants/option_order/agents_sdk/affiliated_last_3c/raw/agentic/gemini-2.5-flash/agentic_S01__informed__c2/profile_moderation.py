import os
import requests

def moderate_profile_text(text: str) -> dict:
    """
    Moderates profile text before account activation using Azure AI Content Safety.
    
    Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")

    url = f"{endpoint}contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [] # Optionally specify blocklists
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    return response.json()

if __name__ == "__main__":
    # Example Usage (Requires AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY env vars)
    # profile_input = "I love this app! It's fantastic. I will hurt anyone who disagrees."
    # try:
    #     moderation_result = moderate_profile_text(profile_input)
    #     print(f"Moderation Result for '{profile_input}':")
    #     print(moderation_result)
    # except requests.exceptions.HTTPError as e:
    #     print(f"Error moderating text: {e.response.text}")
    # except ValueError as e:
    #     print(f"Configuration error: {e}")
    pass
