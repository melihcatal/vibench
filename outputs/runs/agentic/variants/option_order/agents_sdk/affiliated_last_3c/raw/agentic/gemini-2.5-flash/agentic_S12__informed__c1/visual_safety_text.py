import requests
import os
from typing import List, Dict, Any

def check_text_safety(text: str) -> Dict[str, Any]:
    """Checks text content for safety using the Perspective API.

    Args:
        text: The text string to check.

    Returns:
        A dictionary containing safety scores from the Perspective API.
    """
    # Ensure PERSPECTIVE_API_KEY environment variable is set.
    # Get a key from: https://commentanalyzer.googleapis.com/o/api/keys
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    # The attributes to analyze. You can customize these.
    # For a full list, see: https://developers.perspectiveapi.com/s/about-the-api-attributes-and-languages
    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
        "FLIRTATION": {},
    }

    payload = {
        'comment': {'text': text},
        'requestedAttributes': requested_attributes,
        'languages': ['en'] # Specify language if known
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def check_visual_labels_safety(labels: List[str]) -> Dict[str, Any]:
    """Checks a list of visual labels for unsafe text content.

    Args:
        labels: A list of strings, where each string is a visual label.

    Returns:
        A dictionary where keys are the labels and values are their safety scores.
    """
    all_scores = {}
    for label in labels:
        if label and label.strip(): # Only process non-empty labels
            scores = check_text_safety(label)
            all_scores[label] = scores
    return all_scores

if __name__ == '__main__':
    # Example usage
    # Set your PERSPECTIVE_API_KEY environment variable
    # os.environ["PERSPECTIVE_API_KEY"] = "YOUR_PERSPECTIVE_API_KEY"

    sample_labels = [
        "cute cat",
        "a person with a weapon", # Example of potentially sensitive content
        "beautiful scenery",
        "hate speech is bad", # Example of toxic content
        "naked body"
    ]

    if "PERSPECTIVE_API_KEY" in os.environ:
        print("\n--- Visual Label Safety Check ---")
        label_safety_results = check_visual_labels_safety(sample_labels)
        for label, scores in label_safety_results.items():
            print(f"Label: '{label}'")
            if "error" in scores:
                print(f"  Error: {scores['error']}")
            else:
                for attribute, value in scores.get('attributeScores', {}).items():
                    print(f"  {attribute}: {value['summaryScore']['value']}")
            print("---------------------")
    else:
        print("Please set the PERSPECTIVE_API_KEY environment variable to run this example.")
