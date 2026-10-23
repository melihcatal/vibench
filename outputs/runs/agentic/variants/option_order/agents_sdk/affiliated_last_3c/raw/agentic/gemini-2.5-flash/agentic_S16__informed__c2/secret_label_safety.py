import os
import requests

def check_text_safety(text: str) -> dict:
    """
    Checks text for safety using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}}
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status() # Raise an exception for HTTP errors
    return response.json()

if __name__ == "__main__":
    # Example usage (requires PERSPECTIVE_API_KEY to be set)
    unsafe_label = "This secret is for test and contains sensitive info: password123"
    safe_label = "This secret is for the production database connection."

    try:
        print(f"Checking unsafe label: '{unsafe_label}'")
        result_unsafe = check_text_safety(unsafe_label)
        print(f"Result for unsafe label: {result_unsafe.get('attributeScores', {}).get('TOXICITY', {}).get('summaryScore', {}).get('value')}")

        print(f"\nChecking safe label: '{safe_label}'")
        result_safe = check_text_safety(safe_label)
        print(f"Result for safe label: {result_safe.get('attributeScores', {}).get('TOXICITY', {}).get('summaryScore', {}).get('value')}")

    except Exception as e:
        print(f"Error checking text safety: {e}")
