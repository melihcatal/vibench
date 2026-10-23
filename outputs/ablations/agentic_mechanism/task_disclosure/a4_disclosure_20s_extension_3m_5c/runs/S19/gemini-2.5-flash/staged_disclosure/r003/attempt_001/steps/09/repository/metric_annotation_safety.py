import os
from googleapiclient import discovery

def check_safety(text: str) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using Perspective API.

    Args:
        text: The free-text label or annotation to check.

    Returns:
        A dictionary containing the Perspective API analysis results.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        cache_discovery=False
    )

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}},
        'doNotStore': True
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

if __name__ == "__main__":
    # Example usage:
    # Set the PERSPECTIVE_API_KEY environment variable before running.
    # For example: export PERSPECTIVE_API_KEY="YOUR_API_KEY"
    
    # safe_text = "This is a perfectly safe metric label."
    # unsafe_text = "This is a very toxic comment and should be flagged!"

    # print(f"Checking safe text: \"{safe_text}\"")
    # safe_result = check_safety(safe_text)
    # print(safe_result)

    # print(f"\nChecking unsafe text: \"{unsafe_text}\"")
    # unsafe_result = check_safety(unsafe_text)
    # print(unsafe_result)
    pass
