import os
import requests

def check_text_safety(text: str) -> dict:
    """
    Checks text for unsafe content using Google Perspective API.
    Requires PERSPECTIVE_API_KEY environment variable.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
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
        }
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    # Example usage (requires PERSPECTIVE_API_KEY env var)
    # sample_text = "You are an idiot!"
    # result = check_text_safety(sample_text)
    # print(result)
    pass
