
from googleapiclient import discovery
import json

def check_safety(text):
    """
    Checks free-text metric labels or annotations for unsafe text using Google Cloud's Perspective API.

    Args:
        text: The free-text string to analyze.

    Returns:
        A dictionary containing the analysis results from the Perspective API.
    """
    # Replace with your API key or use environment variable (e.g., PERSPECTIVE_API_KEY)
    # Ensure you have enabled the Perspective API in your Google Cloud project
    # and set up authentication.
    API_KEY = "YOUR_PERSPECTIVE_API_KEY" 

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {}
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

if __name__ == "__main__":
    example_text_safe = "This is a perfectly safe metric label."
    example_text_unsafe = "This comment is really hateful and toxic!"

    print(f"Checking text: \"{example_text_safe}\"")
    safe_result = check_safety(example_text_safe)
    print(json.dumps(safe_result, indent=2))

    print(f"\nChecking text: \"{example_text_unsafe}\"")
    unsafe_result = check_safety(example_text_unsafe)
    print(json.dumps(unsafe_result, indent=2))
