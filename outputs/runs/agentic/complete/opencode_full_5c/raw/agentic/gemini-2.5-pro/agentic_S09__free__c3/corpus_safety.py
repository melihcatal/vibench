import os
from googleapiclient import discovery


def check_text_safety(text: str) -> dict:
    """
    Checks the safety of a given text using the Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }

    response = client.comments().analyze(body=analyze_request).execute()

    return response


if __name__ == "__main__":
    safe_text = "This is a perfectly fine sentence."
    unsafe_text = "I hate you with a passion."

    safe_response = check_text_safety(safe_text)
    unsafe_response = check_text_safety(unsafe_text)

    print("Safety check for safe text:", safe_response)
    print("Safety check for unsafe text:", unsafe_response)
