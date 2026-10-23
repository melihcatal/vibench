import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_message_safety(text_payload: str) -> bool:
    """
    Checks if a message payload is safe using the Google Perspective API.
    Returns True if the content is considered safe, False otherwise.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

    analyze_request = {
        'comment': {'text': text_payload},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en']
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
        
        # Consider content unsafe if toxicity score is above a threshold (e.g., 0.7)
        return toxicity_score < 0.7
    except HttpError as e:
        print(f"An error occurred with Perspective API: {e}")
        # Default to safe in case of API error to avoid dropping messages
        return True
    except Exception as e:
        print(f"A general error occurred: {e}")
        return True
