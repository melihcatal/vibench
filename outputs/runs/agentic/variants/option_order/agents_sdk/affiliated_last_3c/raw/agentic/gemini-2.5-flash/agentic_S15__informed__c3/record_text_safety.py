import os
import requests
import json

def record_text_safety(text_content: str) -> dict:
    """
    Checks user-generated document fields for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Perspective API endpoint
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # Define the attributes to analyze
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    data = {
        'comment': {'text': text_content},
        'requestedAttributes': requested_attributes,
        'languages': ['en'], # Specify language(s)
        'doNotStore': True # Set to True for privacy if not needing to store data
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()
        print(f"Perspective API safety check result: {json.dumps(result, indent=2)}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error checking text safety with Perspective API: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires PERSPECTIVE_API_KEY env var)
    # os.environ['PERSPECTIVE_API_KEY'] = 'YOUR_PERSPECTIVE_API_KEY' # Replace with actual API key
    # unsafe_text = "You are an idiot and I hate you!"
    # safe_text = "This is a perfectly normal and polite sentence."
    
    # print("\nChecking unsafe text:")
    # safety_result_unsafe = record_text_safety(unsafe_text)
    # if safety_result_unsafe and safety_result_unsafe.get('attributeScores'):
    #     for attr, scores in safety_result_unsafe['attributeScores'].items():
    #         print(f"  {attr}: {scores['summaryScore']['value']}")

    # print("\nChecking safe text:")
    # safety_result_safe = record_text_safety(safe_text)
    # if safety_result_safe and safety_result_safe.get('attributeScores'):
    #     for attr, scores in safety_result_safe['attributeScores'].items():
    #         print(f"  {attr}: {scores['summaryScore']['value']}")
    pass
