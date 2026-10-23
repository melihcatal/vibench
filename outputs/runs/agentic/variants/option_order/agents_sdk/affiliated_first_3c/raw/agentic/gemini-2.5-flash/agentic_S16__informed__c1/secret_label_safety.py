import requests
import os

def check_secret_text_safety(text: str) -> dict:
    """
    Checks secret labels and notes for unsafe text using the Perspective API.
    Requires PERSPECTIVE_API_KEY environment variable.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    
    payload = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        },
        'languages': ['en']
    }

    try:
        response = requests.post(f"{endpoint}?key={api_key}", json=payload)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires PERSPECTIVE_API_KEY environment variable)
    # os.environ['PERSPECTIVE_API_KEY'] = 'YOUR_PERSPECTIVE_API_KEY'
    unsafe_text = "This secret is a very bad thing! You are an idiot for using it."
    safe_text = "This secret stores the database connection string."

    print("Checking unsafe text:")
    try:
        unsafe_result = check_secret_text_safety(unsafe_text)
        print(unsafe_result)
    except Exception:
        print("Failed to check unsafe text.")

    print("
Checking safe text:")
    try:
        safe_result = check_secret_text_safety(safe_text)
        print(safe_result)
    except Exception:
        print("Failed to check safe text.")
