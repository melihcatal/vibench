import os
import requests

def check_text_safety_perspective(text: str, api_key: str, threshold: float = 0.8) -> dict:
    """
    Checks text for toxicity and other attributes using Perspective API.

    Args:
        text: The text content to analyze.
        api_key: Your Perspective API key.
        threshold: The threshold for flagging content (e.g., 0.8 for 80% confidence).

    Returns:
        A dictionary containing the analysis results.
    """
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=" + api_key
    
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
    }

    data = {
        'comment': {'text': text},
        'requestedAttributes': requested_attributes,
        'languages': ['en'] # Specify languages, e.g., 'en' for English
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        
        # Process and simplify the result
        safety_scores = {}
        for attr, details in result.get('attributeScores', {}).items():
            score = details.get('summaryScore', {}).get('value')
            if score is not None:
                safety_scores[attr] = score
        
        flagged_categories = {attr: score for attr, score in safety_scores.items() if score > threshold}

        return {
            "scores": safety_scores,
            "flagged": bool(flagged_categories),
            "flagged_categories": flagged_categories
        }
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

