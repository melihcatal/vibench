import os
import json
import requests

def check_log_safety(log_message: str) -> dict:
    """
    Checks log message text for unsafe content using the Perspective API.

    Args:
        log_message: The text content of the log message to check.

    Returns:
        A dictionary containing the analysis results from the API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    request_payload = {
        "comment": {"text": log_message},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
        },
    }

    try:
        response = requests.post(url, json=request_payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred calling the Perspective API: {e}")
        return {"error": str(e)}

# Example of how this might be called (not executed):
# if __name__ == '__main__':
#     message = "This is a benign log message about a user login."
#     safety_scores = check_log_safety(message)
#     print(json.dumps(safety_scores, indent=2))
#
#     message_unsafe = "this is an example of a hateful and threatening message"
#     safety_scores_unsafe = check_log_safety(message_unsafe)
#     print(json.dumps(safety_scores_unsafe, indent=2))
