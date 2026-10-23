import requests
import os

def check_payload_safety(text_payload: str) -> dict:
    """Checks decrypted text payloads for unsafe content using Perspective API.

    Args:
        text_payload: The text content to analyze.

    Returns:
        A dictionary containing the analysis results.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Perspective API endpoint for analyzeText
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text_payload},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"], # Specify desired languages
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage:
    # text_to_check = "You are an idiot and I hate you."
    # try:
    #     safety_report = check_payload_safety(text_to_check)
    #     print("Payload Safety Report:")
    #     import json
    #     print(json.dumps(safety_report, indent=2))
    # except Exception as e:
    #     print(f"Error checking payload safety: {e}")
    #     print("Please ensure PERSPECTIVE_API_KEY is set and valid.")

    # text_to_check_safe = "This is a perfectly safe and pleasant message."
    # try:
    #     safety_report_safe = check_payload_safety(text_to_check_safe)
    #     print("\nSafe Payload Safety Report:")
    #     import json
    #     print(json.dumps(safety_report_safe, indent=2))
    # except Exception as e:
    #     print(f"Error checking safe payload safety: {e}")
    #     print("Please ensure PERSPECTIVE_API_KEY is set and valid.")
