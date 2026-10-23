import os
from googleapiclient import discovery

def check_unsafe_text(text):
    """
    Checks free-text metric labels or annotations for unsafe text using Perspective API.

    Args:
        text: The free-text string to analyze.

    Returns:
        A dictionary containing the analysis results from Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
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

if __name__ == '__main__':
    # Example usage (replace with your actual metric labels/annotations)
    sample_text = "This is a great metric label."
    unsafe_text = "This is a terrible and hateful comment."

    print(f"Analysis for '{sample_text}':")
    try:
        result_safe = check_unsafe_text(sample_text)
        print(result_safe)
    except ValueError as e:
        print(f"Error: {e}")

    print(f"
Analysis for '{unsafe_text}':")
    try:
        result_unsafe = check_unsafe_text(unsafe_text)
        print(result_unsafe)
    except ValueError as e:
        print(f"Error: {e}")
