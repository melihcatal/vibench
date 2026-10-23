import requests
import os

def check_text_safety_perspective(text: str) -> dict:
    """Checks free-text metric labels or annotations for unsafe text using the Perspective API.

    Args:
        text: The free-text annotation or label to check.

    Returns:
        A dictionary containing the Perspective API analysis results.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

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
        "languages": ["en"]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Perspective API request failed: {e}"}

if __name__ == "__main__":
    # Example usage
    unsafe_annotation = "This dashboard is showing terrible performance, it's completely broken!"
    safe_annotation = "Performance metrics are showing a steady increase over the last hour."

    print("Checking unsafe annotation...")
    unsafe_result = check_text_safety_perspective(unsafe_annotation)
    print("\n--- Unsafe Annotation Analysis ---")
    print(unsafe_result)
    print("----------------------------------")

    print("\nChecking safe annotation...")
    safe_result = check_text_safety_perspective(safe_annotation)
    print("\n--- Safe Annotation Analysis ---")
    print(safe_result)
    print("------------------------------")
