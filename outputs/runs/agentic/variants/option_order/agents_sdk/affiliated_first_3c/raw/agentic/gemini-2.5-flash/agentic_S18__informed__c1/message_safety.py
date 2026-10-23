import os
import requests
import json

def check_message_safety(text_content: str, api_key: str = None) -> dict:
    """
    Checks the safety of message content using the Perspective API.
    """
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")
        if not api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    payload = {
        "comment": {"text": text_content},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()
        
        safety_scores = {}
        for attribute, details in result.get("attributeScores", {}).items():
            safety_scores[attribute] = details["summaryScore"]["value"]
        
        return safety_scores
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError as e:
        print(f"Error decoding API response: {e}")
        return {"error": "Invalid JSON response from API"}

if __name__ == "__main__":
    # Ensure PERSPECTIVE_API_KEY is set in your environment
    if os.environ.get("PERSPECTIVE_API_KEY"):
        unsafe_text = "You are an idiot and should shut up!"
        safe_text = "Hello, how are you doing today?"

        print("Checking unsafe text:")
        scores_unsafe = check_message_safety(unsafe_text)
        print(json.dumps(scores_unsafe, indent=2))

        print("\nChecking safe text:")
        scores_safe = check_message_safety(safe_text)
        print(json.dumps(scores_safe, indent=2))
    else:
        print("Please set the PERSPECTIVE_API_KEY environment variable to run this example.")
