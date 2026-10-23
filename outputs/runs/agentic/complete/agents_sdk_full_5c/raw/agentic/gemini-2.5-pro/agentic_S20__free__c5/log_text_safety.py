import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_log_message_safety(log_message: str):
    """
    Uses the Google Perspective API to check a log message for toxic content.
    This could be useful for logs that might be displayed to support agents or users.
    """
    api_key = os.environ.get("GOOGLE_PERSPECTIVE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_PERSPECTIVE_API_KEY environment variable not set.")
        return

    try:
        # The API client is built using the Google API Python Client library.
        # It's a generic client that can be used for many Google APIs.
        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            static_discovery=False,
        )

        analyze_request = {
            'comment': {'text': log_message},
            'requestedAttributes': {'TOXICITY': {}}
        }

        print(f"Analyzing message for safety: '{log_message}'")
        response = client.comments().analyze(body=analyze_request).execute()

        toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
        
        print(f"Toxicity Score: {toxicity_score:.4f}")
        if toxicity_score > 0.7:
            print("Result: This message is likely unsafe.")
        else:
            print("Result: This message appears to be safe.")
        
        return toxicity_score

    except HttpError as e:
        print(f"An HTTP error occurred with the Perspective API: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    # Example 1: A potentially problematic message
    unsafe_message = "This is an insulting and hateful thing to say."
    check_log_message_safety(unsafe_message)

    print("-" * 20)

    # Example 2: A standard, safe log message
    safe_message = "Service successfully restarted after deployment."
    check_log_message_safety(safe_message)
