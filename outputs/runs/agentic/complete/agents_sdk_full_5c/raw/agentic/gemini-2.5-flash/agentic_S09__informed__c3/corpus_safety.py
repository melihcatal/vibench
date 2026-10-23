import os
import requests
import json

def check_corpus_safety(text_to_check: str, client_ip: str = "127.0.0.1") -> dict:
    """
    Checks the safety of corpus text using Google's Perspective API.

    Args:
        text_to_check: The text content to analyze for safety.
        client_ip: The IP address of the end user, for better abuse detection.

    Returns:
        A dictionary containing the Perspective API analysis results.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Perspective API endpoint
    # Provider-identifying signal: hostname
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "comment": {"text": text_to_check},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "doNotStore": True,
        "clientToken": client_ip
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    safe_text = "This is a perfectly normal and safe sentence."
    unsafe_text = "You are an idiot and I will hurt you."

    print("Checking safe text:")
    safe_result = check_corpus_safety(safe_text)
    print(json.dumps(safe_result, indent=2))

    print("\nChecking unsafe text:")
    unsafe_result = check_corpus_safety(unsafe_text)
    print(json.dumps(unsafe_result, indent=2))
