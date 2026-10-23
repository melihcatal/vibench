import os
import requests

def check_message_safety(text_content: str) -> dict:
    """Checks message payload text for unsafe content using the Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Perspective API endpoint for analyzeText
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text_content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        }
    }

    try:
        response = requests.post(url, params=params, headers=headers, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    # from your shell, run:
    # export PERSPECTIVE_API_KEY="your-perspective-api-key"
    # python message_safety.py
    safe_text = "This is a polite and friendly message."
    unsafe_text = "You are an idiot!"

    print("Checking safe text:")
    safety_report_safe = check_message_safety(safe_text)
    print(safety_report_safe)

    print("\nChecking unsafe text:")
    safety_report_unsafe = check_message_safety(unsafe_text)
    print(safety_report_unsafe)
