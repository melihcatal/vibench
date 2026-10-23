import os
import googleapiclient.discovery

def moderate_claim(text: str) -> dict:
    """
    Moderates free-text claims or notes using Google Cloud's Perspective API.

    Args:
        text: The free-text claim or note to moderate.

    Returns:
        A dictionary containing the moderation results from the Perspective API.
    """
    # Initialize the Perspective API client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or other authentication methods are configured for googleapiclient.
    client = googleapiclient.discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.environ.get("PERSPECTIVE_API_KEY")
    )

    analyze_request = {
        'comment': {'text': text},
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

if __name__ == "__main__":
    test_claim_toxic = "You are a terrible person and I hate you."
    test_claim_neutral = "This is a neutral statement about the weather."
    test_claim_profane = "What the heck is going on here?"

    print(f"Moderating: \"{test_claim_toxic}\"")
    result_toxic = moderate_claim(test_claim_toxic)
    print(f"Result: {result_toxic}\n")

    print(f"Moderating: \"{test_claim_neutral}\"")
    result_neutral = moderate_claim(test_claim_neutral)
    print(f"Result: {result_neutral}\n")

    print(f"Moderating: \"{test_claim_profane}\"")
    result_profane = moderate_claim(test_claim_profane)
    print(f"Result: {result_profane}\n")
