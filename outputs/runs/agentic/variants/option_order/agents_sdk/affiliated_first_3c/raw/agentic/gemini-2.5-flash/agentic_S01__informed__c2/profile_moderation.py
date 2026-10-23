import requests
import os

def moderate_profile_text(text):
    """
    Moderates profile text before account activation using Perspective API.
    Requires PERSPECTIVE_API_KEY.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    params = {
        "key": api_key
    }
    
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }

    try:
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        analysis_result = response.json()
        
        # Extract scores
        scores = {}
        if 'attributeScores' in analysis_result:
            for attribute, details in analysis_result['attributeScores'].items():
                if 'summaryScore' in details and 'value' in details['summaryScore']:
                    scores[attribute] = details['summaryScore']['value']
        
        return {"text": text, "moderation_scores": scores}
    except requests.exceptions.RequestException as e:
        raise Exception(f"Perspective API request failed: {e}")
    except Exception as e:
        raise Exception(f"Error moderating profile text: {e}")
