import os
from googleapiclient import discovery

def check_unsafe_content(text):
    """
    Checks the given text for unsafe content using Google's Perspective API.

    Args:
        text: The string to check for unsafe content.

    Returns:
        A dictionary containing the analysis results from the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_fields=False,
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}},
        'languages': ['en'], # Specify desired language(s)
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

if __name__ == "__main__":
    example_text_safe = "This is a perfectly safe and friendly message."
    example_text_unsafe = "I hate this! You are terrible!"

    print(f"Checking text: '{example_text_safe}'")
    result_safe = check_unsafe_content(example_text_safe)
    print(f"Result: {result_safe}\n")

    print(f"Checking text: '{example_text_unsafe}'")
    result_unsafe = check_unsafe_content(example_text_unsafe)
    print(f"Result: {result_unsafe}")
