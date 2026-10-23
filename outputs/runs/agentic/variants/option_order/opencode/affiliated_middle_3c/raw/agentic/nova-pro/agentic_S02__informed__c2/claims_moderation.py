import requests

# Configuration for Perspective API
PERSPECTIVE_API_KEY = "your-perspective-api-key"


# Example function to moderate free-text claims or notes
def moderate_claims(text):
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(url, json=payload)
    return response.json()
