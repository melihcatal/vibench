import os
import requests
import json
from typing import List, Dict, Any

# Perspective API endpoint and discovery URL
# The actual endpoint is usually constructed with the API key.
# https://developers.perspectiveapi.com/s/docs-sample-request
PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_text_safety(text_to_analyze: str, client_ip: str = None) -> Dict[str, Any]:
    """Checks selected log message text for unsafe content using the Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_BASE_URL}?key={api_key}"

    request_payload = {
        "comment": {"text": text_to_analyze},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            # Add other attributes as needed based on your safety requirements
        },
        "languages": ["en"], # Specify languages if known, or let API detect
        "doNotStore": True, # Set to True for user-generated content to prevent storage
    }

    headers = {"Content-Type": "application/json"}

    if client_ip:
        # Although Perspective API handles some rate limiting and abuse detection,
        # for sensitive scenarios, passing client_ip can be useful.
        # This is not a standard header, but some APIs might use it for internal tracking.
        # For Perspective, it's typically tied to the API key, not individual client IPs within a request.
        pass

    try:
        response = requests.post(url, headers=headers, data=json.dumps(request_payload))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        if e.response is not None:
            print(f"Response content: {e.response.text}")
        return {"error": str(e), "api_response": e.response.text if e.response else "No response"}

if __name__ == "__main__":
    # Example usage:
    # Set PERSPECTIVE_API_KEY environment variable
    if os.getenv("PERSPECTIVE_API_KEY") is None:
        print("Please set the PERSPECTIVE_API_KEY environment variable.")
    else:
        log_message1 = "This is a normal log message, everything is fine."
        log_message2 = "You are an idiot and should be fired!"
        log_message3 = "System crashed due to an unknown error."

        print(f"\nChecking safety for: '{log_message1}'")
        result1 = check_text_safety(log_message1)
        print(json.dumps(result1, indent=2))

        print(f"\nChecking safety for: '{log_message2}'")
        result2 = check_text_safety(log_message2)
        print(json.dumps(result2, indent=2))

        print(f"\nChecking safety for: '{log_message3}'")
        result3 = check_text_safety(log_message3)
        print(json.dumps(result3, indent=2))
