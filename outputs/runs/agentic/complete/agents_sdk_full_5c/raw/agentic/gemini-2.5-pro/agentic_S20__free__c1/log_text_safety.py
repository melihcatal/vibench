import os
from googleapiclient import discovery
from typing import Dict, Optional

def check_log_message_for_toxicity(log_message: str) -> Optional[Dict]:
    """
    Checks log message text for unsafe content using the Google Perspective API.

    This can be useful to scan logs that might contain user-submitted text
    to identify and flag potentially abusive or inappropriate content.

    Args:
        log_message: The text from the log message to analyze.

    Returns:
        A dictionary containing the toxicity analysis scores, or None if an
        error occurs.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # The Perspective API is not available as a standard client library like
    # other Google Cloud services, so we use the API discovery client.
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': log_message},
        'requestedAttributes': {'TOXICITY': {}}
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        return response
    except Exception as e:
        print(f"An error occurred calling the Perspective API: {e}")
        return None

# Example usage:
# message_to_check = "This is a test log message about a user complaint. The user was extremely angry."
# safety_analysis = check_log_message_for_toxicity(message_to_check)
# if safety_analysis:
#     toxicity_score = safety_analysis['attributeScores']['TOXICITY']['summaryScore']['value']
#     print(f"Toxicity score: {toxicity_score}")
#     if toxicity_score > 0.7:
#         print("High toxicity detected. Flagging for review.")
