import requests
import os

# Perspective API endpoint (publicly known)
PERSPECTIVE_API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_text_safety_perspective(text: str) -> dict:
    """Checks generated visual labels for unsafe text using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"{PERSPECTIVE_API_ENDPOINT}?key={api_key}"

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
    }

    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    result = response.json()

    # Extract relevant scores
    safety_scores = {}
    for attr, details in result.get('attributeScores', {}).items():
        safety_scores[attr.lower()] = details['summaryScore']['value']

    return safety_scores

if __name__ == '__main__':
    # Example usage
    # Ensure PERSPECTIVE_API_KEY environment variable is set
    test_text_safe = "This is a beautiful image of a flower."
    safe_scores = check_text_safety_perspective(test_text_safe)
    print(f"Safety scores for \"{'''test_text_safe'''}\": {safe_scores}")

    test_text_unsafe = "You are an idiot!"
    unsafe_scores = check_text_safety_perspective(test_text_unsafe)
    print(f"Safety scores for \"{'''test_text_unsafe'''}\": {unsafe_scores}")
