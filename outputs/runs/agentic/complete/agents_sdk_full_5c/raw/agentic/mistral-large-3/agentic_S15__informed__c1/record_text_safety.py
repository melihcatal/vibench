from googleapiclient import discovery
import os

def check_text_safety(text: str) -> dict:
    """
    Checks text for unsafe content using Google's Perspective API.
    
    Args:
        text: The text to analyze.
        
    Returns:
        dict: The toxicity analysis results.
    """
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.getenv("PERSPECTIVE_API_KEY"),
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False
    )
    
    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}}
    }
    
    response = client.comments().analyze(body=analyze_request).execute()
    return response