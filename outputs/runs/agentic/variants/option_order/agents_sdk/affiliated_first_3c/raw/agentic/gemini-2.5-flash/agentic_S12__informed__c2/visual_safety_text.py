import os
import requests

def check_text_safety_perspective(text: str) -> dict:
    """Checks generated visual labels for unsafe text using Perspective API.

    Args:
        text: The text to analyze for safety.

    Returns:
        A dictionary with safety scores from Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    requested_attributes = {
        'TOXICITY': {},
        'SEVERE_TOXICITY': {},
        'IDENTITY_ATTACK': {},
        'INSULT': {},
        'PROFANITY': {},
        'THREAT': {},
    }

    data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': requested_attributes
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        
        safety_scores = {}
        for attr, details in result.get('attributeScores', {}).items():
            summary_score = details.get('summaryScore', {}).get('value')
            safety_scores[attr] = summary_score
        return safety_scores
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage
    # Ensure PERSPECTIVE_API_KEY is set for authentication
    test_text_safe = "This is a beautiful image."
    test_text_unsafe = "You are an idiot."

    print(f"Checking safety for \"{test_text_safe}\":")
    safe_results = check_text_safety_perspective(test_text_safe)
    print(safe_results)

    print(f"\nChecking safety for \"{test_text_unsafe}\":")
    unsafe_results = check_text_safety_perspective(test_text_unsafe)
    print(unsafe_results)
