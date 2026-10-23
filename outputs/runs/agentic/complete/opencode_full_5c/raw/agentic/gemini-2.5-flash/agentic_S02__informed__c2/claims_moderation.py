import os
import requests
import json

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def moderate_claims_text(text: str) -> dict:
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_ENDPOINT}?key={PERSPECTIVE_API_KEY}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Example usage:
    # Set environment variable PERSPECTIVE_API_KEY
    # claims_note = "This is a test claim. I hate this product!"
    # moderation_result = moderate_claims_text(claims_note)
    # print(json.dumps(moderation_result, indent=2))
    pass
