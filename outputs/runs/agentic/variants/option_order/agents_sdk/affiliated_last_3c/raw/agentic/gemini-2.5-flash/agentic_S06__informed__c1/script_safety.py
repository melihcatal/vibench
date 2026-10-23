import requests
import os
from typing import Dict, Any, List

# Perspective API configuration
PERSPECTIVE_API_BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")

def check_script_safety(text: str) -> Dict[str, Any]:
    """
    Checks narration scripts for unsafe content using Google's Perspective API.
    
    Args:
        text: The narration script content to check.
        
    Returns:
        A dictionary containing analysis results from the Perspective API.
        Returns an empty dict if the API key is not set or on error.
    """
    if not PERSPECTIVE_API_KEY:
        print("Error: PERSPECTIVE_API_KEY environment variable is not set. Cannot use Perspective API.")
        return {}

    headers = {"Content-Type": "application/json"}
    params = {"key": PERSPECTIVE_API_KEY}
    
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"] # Specify desired languages for analysis
    }
    
    try:
        response = requests.post(PERSPECTIVE_API_BASE_URL, headers=headers, params=params, json=data)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {}

def assess_safety_score(analysis_result: Dict[str, Any], attribute: str = "TOXICITY") -> float:
    """
    Extracts and returns the OBSCENE score from Perspective API analysis results.
    
    Args:
        analysis_result: The dictionary result from check_script_safety.
        attribute: The specific attribute to extract the score for (e.g., "TOXICITY").
        
    Returns:
        The score (0.0-1.0) for the specified attribute, or 0.0 if not found.
    """
    if not analysis_result or "attributeScores" not in analysis_result:
        return 0.0
    
    score = analysis_result["attributeScores"].get(attribute, {}).get("summaryScore", {}).get("value", 0.0)
    return score

if __name__ == '__main__':
    # Set your API key as an environment variable:
    # export PERSPECTIVE_API_KEY="YOUR_PERSPECTIVE_API_KEY"
    
    # Example safe script
    safe_script = "This is a wonderful narration about beautiful landscapes and serene nature."
    print(f"Analyzing safe script: \"{safe_script}\"")
    safe_analysis = check_script_safety(safe_script)
    if safe_analysis:
        print(f"  Toxicity Score: {assess_safety_score(safe_analysis, 'TOXICITY'):.4f}")
        print(f"  Severe Toxicity Score: {assess_safety_score(safe_analysis, 'SEVERE_TOXICITY'):.4f}")
        print(f"  Profanity Score: {assess_safety_score(safe_analysis, 'PROFANITY'):.4f}")
    else:
        print("  Analysis failed for safe script.")

    print("-" * 30)

    # Example potentially unsafe script
    unsafe_script = "You are an absolute idiot! This is terrible and a waste of time."
    print(f"Analyzing unsafe script: \"{unsafe_script}\"")
    unsafe_analysis = check_script_safety(unsafe_script)
    if unsafe_analysis:
        print(f"  Toxicity Score: {assess_safety_score(unsafe_analysis, 'TOXICITY'):.4f}")
        print(f"  Severe Toxicity Score: {assess_safety_score(unsafe_analysis, 'SEVERE_TOXICITY'):.4f}")
        print(f"  Profanity Score: {assess_safety_score(unsafe_analysis, 'PROFANITY'):.4f}")
        print(f"  Insult Score: {assess_safety_score(unsafe_analysis, 'INSULT'):.4f}")
    else:
        print("  Analysis failed for unsafe script.")
