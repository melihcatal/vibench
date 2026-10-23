import os
from googleapiclient import discovery

def check_message_for_safety(text: str) -> dict:
    """
    Checks log message text for unsafe content using the Perspective API.

    Args:
        text: The log message to analyze.

    Returns:
        A dictionary containing the analysis results.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
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
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}},
        'languages': ['en']
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {}
        for attribute, data in response['attributeScores'].items():
            scores[attribute] = data['summaryScore']['value']
        return scores
    except Exception as e:
        print(f"Error calling Perspective API: {e}")
        return {}

if __name__ == '__main__':
    # Example log message that might contain user-generated content
    unsafe_log_message = "User 'testuser' submitted a review with hateful and insulting content."
    safe_log_message = "User 'testuser' updated their profile successfully."

    print(f"Analyzing message: '{unsafe_log_message}'")
    safety_scores_unsafe = check_message_for_safety(unsafe_log_message)
    print(f"Safety Scores: {safety_scores_unsafe}")

    print("\n" + "="*20 + "\n")

    print(f"Analyzing message: '{safe_log_message}'")
    safety_scores_safe = check_message_for_safety(safe_log_message)
    print(f"Safety Scores: {safety_scores_safe}")
