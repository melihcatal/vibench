import os
import googleapiclient.discovery

def check_log_safety(log_message: str):
    """
    Checks the given log message for unsafe content using Google's Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = googleapiclient.discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False
    )

    analyze_request = {
        'comment': {'text': log_message},
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
    # Example usage (replace with actual log messages)
    unsafe_log = "This is a really bad and hateful comment."
    safe_log = "User logged in successfully."

    print("Checking unsafe log message:")
    unsafe_result = check_log_safety(unsafe_log)
    print(unsafe_result)

    print("\nChecking safe log message:")
    safe_result = check_log_safety(safe_log)
    print(safe_result)
