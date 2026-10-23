import os
import requests
import json

def check_text_safety_perspective(text: str) -> dict:
    """
    Checks secret labels and notes for unsafe text using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {}
    }

    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": requested_attributes
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "details": response.text if response else "No response"}

if __name__ == "__main__":
    # Set PERSPECTIVE_API_KEY environment variable

    sample_unsafe_text = "This is a terrible secret. You are an idiot for using it."
    sample_safe_text = "This is a secure secret for production environment."

    if os.environ.get("PERSPECTIVE_API_KEY"):
        print("Checking unsafe text...")
        unsafe_results = check_text_safety_perspective(sample_unsafe_text)
        print("\n--- Unsafe Text Analysis ---")
        print(json.dumps(unsafe_results, indent=2))

        print("\nChecking safe text...")
        safe_results = check_text_safety_perspective(sample_safe_text)
        print("\n--- Safe Text Analysis ---")
        print(json.dumps(safe_results, indent=2))
    else:
        print("PERSPECTIVE_API_KEY environment variable not set. Skipping safety check example.")
