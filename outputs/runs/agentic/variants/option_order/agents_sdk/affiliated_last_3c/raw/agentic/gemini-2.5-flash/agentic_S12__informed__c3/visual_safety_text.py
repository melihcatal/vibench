import os
import requests
from typing import List, Dict, Any

def check_text_safety(text: str, client_ip: str = "127.0.0.1") -> Dict[str, Any]:
    """
    Checks generated visual labels and descriptions for unsafe text using Perspective API.
    """
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    
    # Perspective API can be sensitive to request body structure
    data = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        },
        'spanAnnotations': False,
        'clientToken': client_ip # Optional, for client-side API usage tracking
    }
    
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, params={'key': api_key}, json=data, headers=headers)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        
        analysis_results = response.json()
        
        scores = {}
        for attribute, value in analysis_results.get('attributeScores', {}).items():
            scores[attribute] = value.get('summaryScore', {}).get('value')
        
        return scores
    except requests.exceptions.RequestException as e:
        print(f"Error checking text safety with Perspective API: {e}")
        return {}

if __name__ == '__main__':
    # This example requires PERSPECTIVE_API_KEY to be set.
    # text_to_check = "This is a great comment! You are an idiot."
    # safety_scores = check_text_safety(text_to_check)
    # print(f"Text: '{text_to_check}'")
    # print(f"Safety Scores: {safety_scores}")
    pass
