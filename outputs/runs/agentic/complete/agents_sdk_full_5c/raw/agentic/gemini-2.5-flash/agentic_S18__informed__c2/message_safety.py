import requests
import os
import json

def check_text_safety_perspective_api(text: str) -> dict:
    """Checks text content for safety using the Perspective API.
    Requires a GOOGLE_CLOUD_PROJECT_ID and PERSPECTIVE_API_KEY (obtained from Google Cloud API Key).
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
        },
        'languages': ['en'],
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()
        print(f"Perspective API Safety Check Result: {json.dumps(result, indent=2)}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        if response is not None:
            print(f"Response content: {response.text}")
        raise

if __name__ == "__main__":
    sample_unsafe_text = "You are an idiot and I hate you!"
    sample_safe_text = "This is a perfectly normal and safe message."

    if not os.getenv("PERSPECTIVE_API_KEY"):
        print("Please set the PERSPECTIVE_API_KEY environment variable (Google Cloud API Key with Perspective API enabled).")
    else:
        print("\n--- Checking unsafe text ---")
        check_text_safety_perspective_api(sample_unsafe_text)
        print("\n--- Checking safe text ---")
        check_text_safety_perspective_api(sample_safe_text)
