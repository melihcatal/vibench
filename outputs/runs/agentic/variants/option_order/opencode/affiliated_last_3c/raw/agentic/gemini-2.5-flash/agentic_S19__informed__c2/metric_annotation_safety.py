import os
import requests
import json


def check_text_safety(text: str) -> dict:
    """Checks free-text metric labels or annotations for unsafe text using the Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )
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
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        },
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()


# Example usage (assuming PERSPECTIVE_API_KEY is set)
# if __name__ == "__main__":
#     unsafe_text = "This is a terrible dashboard, it's completely useless!"
#     safety_report = check_text_safety(unsafe_text)
#     print(json.dumps(safety_report, indent=2))
