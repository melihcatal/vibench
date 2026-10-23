import os
import requests
import json

def check_text_safety(text: str) -> dict:
    """
    Checks the safety of a text using Google's Perspective API.
    
    Args:
        text: The text to analyze.
        
    Returns:
        A dictionary with toxicity analysis.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
        
    # Provider-specific API hostname
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    request_payload = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }
    
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, data=json.dumps(request_payload), headers=headers)
    response.raise_for_status()
    
    response_data = response.json()
    
    toxicity_score = response_data['attributeScores']['TOXICITY']['summaryScore']['value']
    
    return {
        'text': text,
        'toxicity_score': toxicity_score,
        'is_toxic': toxicity_score > 0.7
    }
