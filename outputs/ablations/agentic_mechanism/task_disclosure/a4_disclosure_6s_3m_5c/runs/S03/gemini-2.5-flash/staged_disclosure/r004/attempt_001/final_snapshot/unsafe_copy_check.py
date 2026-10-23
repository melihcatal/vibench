import os
from googleapiclient import discovery

def check_unsafe_content(text: str) -> dict:
    """
    Checks the given text for unsafe content using the Perspective API.

    Args:
        text: The text to be analyzed.

    Returns:
        A dictionary containing the analysis results.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
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
            'THREAT': {},
        }
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

if __name__ == "__main__":
    # Example usage (replace with actual localized copy)
    example_text = "You are an idiot!"
    result = check_unsafe_content(example_text)
    print(result)
