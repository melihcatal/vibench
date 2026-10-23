import os
import requests

def check_text_safety(text: str) -> dict:
    """Checks text for unsafe content using the Perspective API.
    
    Args:
        text: The text to be checked for safety.
        
    Returns:
        A dictionary containing the Perspective API response.
    """
    perspective_api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # Perspective API endpoint
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={perspective_api_key}"

    # Request body for Perspective API
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
        'languages': ['en']
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors

    return response.json()

def secret_label_safety(labels: dict, notes: str) -> dict:
    """Checks secret labels and notes for unsafe text using Perspective API.
    
    Args:
        labels: A dictionary of secret labels.
        notes: A string containing secret notes.
        
    Returns:
        A dictionary with safety analysis results for labels and notes.
    """
    all_text = " "
    if labels:
        for key, value in labels.items():
            all_text += f"{key} {value} "
    if notes:
        all_text += notes
    
    if not all_text.strip():
        return {"message": "No text to analyze.", "analysis_results": {}}

    analysis_results = check_text_safety(all_text.strip())
    
    return {"analysis_results": analysis_results}

if __name__ == "__main__":
    # Example usage:
    # Set PERSPECTIVE_API_KEY environment variable
    # example_labels = {"department": "finance", "risk": "high"}
    # example_notes = "This secret is highly sensitive and critical for production access. Do NOT share!"
    # safety_report = secret_label_safety(example_labels, example_notes)
    # print(f"Safety Report: {safety_report}")
    pass
