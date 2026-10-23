import requests
import os

def check_text_safety(text: str, api_key: str) -> dict:
    """Checks text for safety using the Perspective API."""
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=" + api_key
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
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        if response.status_code:
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
        return {}

def check_secret_labels_for_safety(labels: dict, notes: str = "") -> dict:
    """Checks secret labels and optional notes for unsafe text using Perspective API."""
    perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not perspective_api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    safety_results = {}
    for key, value in labels.items():
        label_text = f"{key}: {value}"
        result = check_text_safety(label_text, perspective_api_key)
        if result:
            safety_results[f"label_{key}"] = result.get("attributeScores")

    if notes:
        notes_result = check_text_safety(notes, perspective_api_key)
        if notes_result:
            safety_results["notes"] = notes_result.get("attributeScores")
    
    return safety_results

if __name__ == "__main__":
    # Set PERSPECTIVE_API_KEY environment variable before running
    # For example: export PERSPECTIVE_API_KEY="your-perspective-api-key"
    if "PERSPECTIVE_API_KEY" not in os.environ:
        print("Please set the PERSPECTIVE_API_KEY environment variable.")
    else:
        example_labels = {"environment": "prod", "owner": "dev-team", "description": "Contains sensitive user data."}
        example_notes = "This secret is critical and should be handled with extreme care. Do not expose."
        try:
            results = check_secret_labels_for_safety(example_labels, example_notes)
            print(f"Safety Check Results: {results}")
        except Exception as e:
            print(f"Error checking secret label safety: {e}")
