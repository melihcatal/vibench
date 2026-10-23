import os
import requests

def check_message_safety(text_content: str) -> dict:
    """Checks the safety of text content using the Perspective API.
    Requires PERSPECTIVE_API_KEY environment variable.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "comment": {"text": text_content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"]
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage
    unsafe_text = "You are an idiot and I hate you!"
    safe_text = "This is a perfectly fine and friendly message."
    
    try:
        print("\nChecking unsafe text:")
        unsafe_result = check_message_safety(unsafe_text)
        print(unsafe_result)

        print("\nChecking safe text:")
        safe_result = check_message_safety(safe_text)
        print(safe_result)

    except ValueError as e:
        print(f"Error: {e}")
