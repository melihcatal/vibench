import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_log_content_safety(text: str) -> dict:
    """
    Analyzes log text for unsafe content using the Google Perspective API.

    Args:
        text: The log message text to analyze.

    Returns:
        A dictionary with toxicity scores.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    try:
        # Note: discovery.build is a dynamic client builder from google-api-python-client
        service = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            static_discovery=False, # Use dynamic discovery
        )
    except HttpError as e:
        raise RuntimeError(f"Failed to build Perspective API client: {e}") from e

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
        },
        'languages': ['en']
    }

    try:
        response = service.comments().analyze(body=analyze_request).execute()
        scores = {}
        for attr, value in response['attributeScores'].items():
            scores[attr] = value['summaryScore']['value']
        return scores
    except HttpError as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example log messages
    safe_log = "User 'testuser' successfully updated profile."
    unsafe_log = "User 'hacker123' initiated a threatening and obscene sql injection attack."

    print(f"Analyzing safe log message: '{safe_log}'")
    try:
        safe_scores = check_log_content_safety(safe_log)
        print(safe_scores)
    except (ValueError, RuntimeError) as e:
        print(e)
    
    print("-" * 20)
    
    print(f"Analyzing unsafe log message: '{unsafe_log}'")
    try:
        unsafe_scores = check_log_content_safety(unsafe_log)
        print(unsafe_scores)
    except (ValueError, RuntimeError) as e:
        print(e)
