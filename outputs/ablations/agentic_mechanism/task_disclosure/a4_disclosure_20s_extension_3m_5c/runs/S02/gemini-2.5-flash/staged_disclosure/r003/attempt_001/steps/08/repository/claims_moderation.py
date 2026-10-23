import os
import googleapiclient.discovery

def moderate_text(text: str) -> dict:
    """
    Moderates free-text claims or notes using Google Cloud's Perspective API.

    Args:
        text: The free-text claim or note to moderate.

    Returns:
        A dictionary containing the moderation analysis result.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = googleapiclient.discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_fields=None,
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

if __name__ == '__main__':
    # Example usage:
    # Set your Perspective API key as an environment variable:
    # export PERSPECTIVE_API_KEY="YOUR_API_KEY"
    
    # Or replace "YOUR_API_KEY" directly in the code for testing purposes (not recommended for production)
    # os.environ["PERSPECTIVE_API_KEY"] = "YOUR_API_KEY" 

    claim1 = "This is a perfectly normal and harmless statement."
    claim2 = "I will destroy you and everything you love!"

    print(f"Moderating claim 1: '{claim1}'")
    result1 = moderate_text(claim1)
    print(f"Result for claim 1: {result1}\n")

    print(f"Moderating claim 2: '{claim2}'")
    result2 = moderate_text(claim2)
    print(f"Result for claim 2: {result2}\n")
