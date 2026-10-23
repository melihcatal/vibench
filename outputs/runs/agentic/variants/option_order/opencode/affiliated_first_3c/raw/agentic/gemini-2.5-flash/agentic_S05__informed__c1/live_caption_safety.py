import requests
import os


def check_content_safety(text: str) -> dict:
    """
    Checks live transcript text for unsafe content using the Perspective API.
    Service: Perspective API
    Interface: REST (requests library)
    Auth: PERSPECTIVE_API_KEY (from environment variable)
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

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

    # Provider-identifying signal: URL hostname "commentanalyzer.googleapis.com"
    response = requests.post(url, params=params, json=data)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Make sure PERSPECTIVE_API_KEY is set in your environment

    safe_caption = "This is a wonderful day!"
    unsafe_caption = "You are an idiot and I hate you."

    print(f"Checking safety for: '{safe_caption}'")
    safe_result = check_content_safety(safe_caption)
    print(f"Result: {safe_result}\n")

    print(f"Checking safety for: '{unsafe_caption}'")
    unsafe_result = check_content_safety(unsafe_caption)
    print(f"Result: {unsafe_result}")
