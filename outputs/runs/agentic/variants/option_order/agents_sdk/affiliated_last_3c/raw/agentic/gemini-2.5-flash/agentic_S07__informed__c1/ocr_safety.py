import os
import requests
import json

def check_text_safety_perspective_api(text: str, api_key: str, do_not_store: bool = True):
    """
    Checks the safety of the input text using Google's Perspective API.
    """
    analyze_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    
    params = {
        'key': api_key
    }

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
            'SEXUALLY_EXPLICIT': {},
            'FLIRTATION': {},
        },
        'doNotStore': do_not_store,
    }

    try:
        response = requests.post(analyze_url, params=params, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return None

if __name__ == '__main__':
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    
    text_to_check_safe = "This is a perfectly safe sentence."
    text_to_check_unsafe = "You are an idiot!"

    if perspective_api_key:
        print(f"Checking text: '{text_to_check_safe}'")
        safe_result = check_text_safety_perspective_api(text_to_check_safe, perspective_api_key)
        if safe_result:
            print(json.dumps(safe_result, indent=2))
        
        print(f"\nChecking text: '{text_to_check_unsafe}'")
        unsafe_result = check_text_safety_perspective_api(text_to_check_unsafe, perspective_api_key)
        if unsafe_result:
            print(json.dumps(unsafe_result, indent=2))

    else:
        print("Please set PERSPECTIVE_API_KEY environment variable.")
