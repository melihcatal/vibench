import os
import requests

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")


def moderate_text_claim(text: str) -> dict:
    if not PERSPECTIVE_API_KEY:
        raise ValueError("Missing PERSPECTIVE_API_KEY environment variable.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
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

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error moderating text with Perspective API: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    test_claim_toxic = "This is a very insulting and bad comment."
    moderation_result = moderate_text_claim(test_claim_toxic)
    import json

    print(
        "Moderation Result for toxic comment:", json.dumps(moderation_result, indent=2)
    )

    test_claim_neutral = "This is a perfectly normal user note."
    moderation_result = moderate_text_claim(test_claim_neutral)
    print(
        "Moderation Result for neutral comment:",
        json.dumps(moderation_result, indent=2),
    )
