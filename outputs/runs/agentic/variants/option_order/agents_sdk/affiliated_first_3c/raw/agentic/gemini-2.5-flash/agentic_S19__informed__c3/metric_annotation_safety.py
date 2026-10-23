import os
import requests
import json

def check_annotation_safety(text: str, api_key: str = None) -> dict:
    """Checks free-text metric labels or annotations for unsafe text using Perspective API.

    Args:
        text: The free-text annotation or label to check.
        api_key: Your Perspective API key. If None, it tries to get from PERSPECTIVE_API_KEY environment variable.

    Returns:
        A dictionary containing the safety analysis results from Perspective API.
    """
    if api_key is None:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")
        if not api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable not set and no API key provided.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {"Content-Type": "application/json"}
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
        "doNotStore": True # Recommended for sensitive data
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (requires PERSPECTIVE_API_KEY environment variable to be set)
    # unsafe_text = "This metric is showing a terrible performance and the system is garbage!"
    # safe_text = "The system performance metric is stable."

    # try:
    #     print("\n--- Unsafe Text Analysis ---")
    #     results_unsafe = check_annotation_safety(unsafe_text)
    #     print(json.dumps(results_unsafe, indent=2))

    #     print("\n--- Safe Text Analysis ---")
    #     results_safe = check_annotation_safety(safe_text)
    #     print(json.dumps(results_safe, indent=2))

    # except ValueError as e:
    #     print(e)
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
    pass
