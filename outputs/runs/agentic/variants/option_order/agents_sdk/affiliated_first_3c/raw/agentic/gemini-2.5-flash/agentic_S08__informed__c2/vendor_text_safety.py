import requests
import os
import json

def moderate_vendor_text_safety(text_to_moderate: str) -> dict:
    """
    Moderates vendor notes or memo fields using Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "comment": {"text": text_to_moderate},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage:
    # Set PERSPECTIVE_API_KEY environment variable
    #
    # text = "This vendor is terrible! Absolutely horrible service and rude staff."
    # moderation_results = moderate_vendor_text_safety(text)
    # print(json.dumps(moderation_results, indent=2))
    #
    # text_clean = "All good with the vendor, prompt delivery."
    # moderation_results_clean = moderate_vendor_text_safety(text_clean)
    # print(json.dumps(moderation_results_clean, indent=2))
    pass
