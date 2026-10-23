import os
import requests
import json

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def moderate_text_claim(text_claim: str) -> dict:
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_ENDPOINT}?key={PERSPECTIVE_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        'comment': {'text': text_claim},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'THREAT': {},
            'SEXUALLY_EXPLICIT': {},
            'FLIRTATION': {},
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Error moderating claim: {e}"}

if __name__ == '__main__':
    # Example usage:
    # export PERSPECTIVE_API_KEY="YOUR_PERSPECTIVE_API_KEY"
    # test_claim_1 = "This is a perfectly normal comment."
    # test_claim_2 = "You are an idiot and should go to hell!"
    #
    # print("Moderating claim 1:")
    # result1 = moderate_text_claim(test_claim_1)
    # print(json.dumps(result1, indent=2))
    #
    # print("\nModerating claim 2:")
    # result2 = moderate_text_claim(test_claim_2)
    # print(json.dumps(result2, indent=2))
    pass
