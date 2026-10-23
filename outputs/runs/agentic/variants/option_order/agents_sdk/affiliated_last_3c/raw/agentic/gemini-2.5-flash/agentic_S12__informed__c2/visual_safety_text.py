import os
import requests
import json

def check_text_safety_perspective_api(text: str) -> dict:
    """Checks generated visual labels for unsafe text using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    # Supported attribute types can be found in Perspective API documentation
    # https://developers.perspectiveapi.com/s/about-the-api-attributes
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {}
    }

    payload = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    result = response.json()
    
    # Extract scores
    safety_results = {}
    attribute_scores = result.get("attributeScores", {})
    for attr, scores_data in attribute_scores.items():
        summary_score = scores_data.get("summaryScore", {}).get("value")
        if summary_score is not None:
            safety_results[attr] = summary_score # Score is between 0 and 1

    return safety_results

if __name__ == '__main__':
    # Example usage
    # Ensure PERSPECTIVE_API_KEY environment variable is set
    sample_text = "This is a wonderful image, but some parts are quite disturbing."
    
    try:
        safety_scores = check_text_safety_perspective_api(sample_text)
        print(f"Text Safety Scores (Perspective API): {safety_scores}")

        unsafe_text = "You are an idiot!"
        unsafe_scores = check_text_safety_perspective_api(unsafe_text)
        print(f"Unsafe Text Safety Scores (Perspective API): {unsafe_scores}")

    except Exception as e:
        print(f"Error checking text safety: {e}")
        print("Please ensure PERSPECTIVE_API_KEY environment variable is set and has access to Perspective API.")
