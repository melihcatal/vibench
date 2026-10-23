import os
import requests

# Perspective API configuration
PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def record_text_safety(text_content: str) -> dict:
    """Checks user-generated document fields for unsafe content using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_BASE_URL}?key={api_key}"

    request_body = {
        'comment': {'text': text_content},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'THREAT': {},
            'SEXUALLY_EXPLICIT': {},
            'FLIRTATION': {},
            'INSULT': {},
            'PROFANITY': {},
        },
        'languages': ['en']
    }

    try:
        response = requests.post(url, json=request_body)
        response.raise_for_status() # Raise an exception for bad status codes
        analysis_results = response.json()
        print("Content safety check completed successfully with Perspective API.")
        return analysis_results
    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety with Perspective API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage
    # Ensure PERSPECTIVE_API_KEY environment variable is set
    unsafe_text = "You are an idiot and should not speak."
    safety_report = record_text_safety(unsafe_text)
    import json
    print(json.dumps(safety_report, indent=2))

    safe_text = "Hello, how are you today? This is a lovely day."
    safety_report_safe = record_text_safety(safe_text)
    print(json.dumps(safety_report_safe, indent=2))
