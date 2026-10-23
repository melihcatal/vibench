import os
import requests


def check_label_safety(text: str) -> dict:
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
        },
        "languages": ["en"],
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


if __name__ == "__main__":
    unsafe_text = "This secret contains some really bad words like damn and hell."
    safe_text = "This secret is for database connection."

    try:
        print("Checking unsafe text:")
        result = check_label_safety(unsafe_text)
        print(result)

        print("\nChecking safe text:")
        result = check_label_safety(safe_text)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
