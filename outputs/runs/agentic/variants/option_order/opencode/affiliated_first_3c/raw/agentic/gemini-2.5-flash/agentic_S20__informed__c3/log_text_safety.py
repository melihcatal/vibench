import requests
import os


def check_log_text_safety(log_message_text):
    """
    Checks selected log message text for unsafe content using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + api_key
    )

    data = {
        "comment": {"text": log_message_text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    return response.json()


if __name__ == "__main__":
    # Example usage:
    # Ensure PERSPECTIVE_API_KEY environment variable is set.
    # unsafe_text = "This is a test message with some potentially toxic content."
    # safety_analysis = check_log_text_safety(unsafe_text)
    # print(safety_analysis)
    pass
