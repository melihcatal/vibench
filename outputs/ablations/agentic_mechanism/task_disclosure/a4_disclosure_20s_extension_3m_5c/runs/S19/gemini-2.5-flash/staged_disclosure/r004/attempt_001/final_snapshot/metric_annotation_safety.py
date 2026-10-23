
import os
from googleapiclient import discovery

def check_text_safety(text: str) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using Google Cloud Perspective API.

    Args:
        text: The free-text label or annotation to check.

    Returns:
        A dictionary containing the Perspective API analysis result.
        Returns an error message if the API key is not set or if there's an API error.
    """
    # Replace with your actual Perspective API key
    # You can obtain an API key from the Google Cloud Console.
    # It's recommended to store your API key securely, e.g., in an environment variable.
    API_KEY = os.environ.get("PERSPECTIVE_API_KEY", "YOUR_PERSPECTIVE_API_KEY")

    if API_KEY == "YOUR_PERSPECTIVE_API_KEY":
        return {"error": "PERSPECTIVE_API_KEY not set. Please replace 'YOUR_PERSPECTIVE_API_KEY' or set the environment variable."}

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_fields=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
            'SEXUALLY_EXPLICIT': {},
            'FLIRTATION': {},
        }
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        return response
    except Exception as e:
        return {"error": f"Perspective API error: {e}"}

if __name__ == '__main__':
    # Example Usage:
    # Set your API key as an environment variable or replace the placeholder
    # For example: export PERSPECTIVE_API_KEY="YOUR_API_KEY"

    # text_to_check = "This is a perfectly safe metric label."
    # result = check_text_safety(text_to_check)
    # print(f"Analysis for '{text_to_check}':")
    # print(result)

    # unsafe_text = "This is a hateful comment."
    # unsafe_result = check_text_safety(unsafe_text)
    # print(f"\nAnalysis for '{unsafe_text}':")
    # print(unsafe_result)
    pass
