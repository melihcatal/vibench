import requests

# Perspective API for vendor note moderation (later-step)
API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_vendor_text(text):
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(API_URL, params={"key": API_KEY}, json=payload).json()
    toxicity = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    # Threshold can be tuned
    if toxicity > 0.5:
        raise ValueError("Vendor note contains unsafe language")
    return text
