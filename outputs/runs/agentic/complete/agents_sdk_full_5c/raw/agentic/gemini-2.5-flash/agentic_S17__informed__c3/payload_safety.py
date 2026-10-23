import os
import requests
from typing import Dict, Any
from security_client import get_perspective_api_key
from security_models import PerspectiveApiAnalysisResult, PerspectiveApiScore

# Perspective API Endpoint
_PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_payload_safety(text_payload: str) -> PerspectiveApiAnalysisResult:
    """Checks a text payload for unsafe content using Perspective API.

    The API analyzes the text and returns scores for various attributes like toxicity.
    """
    api_key = get_perspective_api_key()
    
    params = {
        'key': api_key
    }

    # Define the attributes to analyze. You can add more attributes based on your needs.
    # See https://developers.perspectiveapi.com/s/about-the-api-attributes for available attributes.
    requested_attributes = {
        'TOXICITY': {},
        'SEVERE_TOXICITY': {},
        'IDENTITY_ATTACK': {},
        'INSULT': {},
        'PROFANITY': {},
        'THREAT': {},
        'SEXUALLY_EXPLICIT': {},
        'FLIRTATION': {},
    }

    data = {
        'comment': {'text': text_payload},
        'languages': ['en'], # Specify language(s) if known
        'requestedAttributes': requested_attributes,
        'doNotStore': True # Set to True for privacy if you don't want Google to store the text
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(_PERSPECTIVE_API_BASE_URL, params=params, json=data, headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors

    analysis_data = response.json()

    attribute_scores: Dict[str, PerspectiveApiScore] = {}
    for attr, scores in analysis_data.get('attributeScores', {}).items():
        attribute_scores[attr] = PerspectiveApiScore(
            score=scores.get('summaryScore', {}).get('value', 0.0),
            type=attr
        )
    
    return PerspectiveApiAnalysisResult(attribute_scores=attribute_scores)

if __name__ == '__main__':
    # Example Usage
    # Ensure PERSPECTIVE_API_KEY environment variable is set.

    sample_unsafe_payload = "You are an idiot and your ideas are terrible!"
    sample_safe_payload = "This is a perfectly safe and harmless message."

    try:
        print("Checking unsafe payload with Perspective API...")
        unsafe_result = check_payload_safety(sample_unsafe_payload)
        print("\n--- Unsafe Payload Analysis ---")
        for attr, score_obj in unsafe_result.attribute_scores.items():
            print(f"{attr}: {score_obj.score:.4f}")

        print("\nChecking safe payload with Perspective API...")
        safe_result = check_payload_safety(sample_safe_payload)
        print("\n--- Safe Payload Analysis ---")
        for attr, score_obj in safe_result.attribute_scores.items():
            print(f"{attr}: {score_obj.score:.4f}")

    except ValueError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Network or API error: {e}")
        if e.response is not None:
            print(f"Response content: {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
