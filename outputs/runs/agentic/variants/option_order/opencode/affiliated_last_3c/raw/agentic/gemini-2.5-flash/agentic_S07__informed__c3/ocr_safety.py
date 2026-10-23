import requests
import os


def check_safety(text: str, api_key: str) -> dict:
    """
    Checks the input text for unsafe content using Perspective API.
    """
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}
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

    response = requests.post(url, params=params, json=data)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    test_text = "You are an idiot."
    # safety_analysis = check_safety(test_text, perspective_api_key)
    # import json
    # print(json.dumps(safety_analysis, indent=2))
