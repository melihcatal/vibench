import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError

def check_text_safety(text: str) -> dict:
    """
    Analyzes text for toxicity using the Google Perspective API.
    
    Returns a dictionary of attribute scores.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
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
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}}
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {
            attr: response['attributeScores'][attr]['summaryScore']['value']
            for attr in response['attributeScores']
        }
        return scores
    except HttpError as e:
        print(f"Perspective API error: {e}")
        return {"error": str(e)}

def is_content_safe(text: str, toxicity_threshold: float = 0.7) -> bool:
    """
    Determines if content is safe based on a toxicity threshold.
    """
    safety_scores = check_text_safety(text)
    if "error" in safety_scores:
        return True # Fail open

    toxicity_score = safety_scores.get("TOXICITY", 0.0)
    return toxicity_score < toxicity_threshold

if __name__ == '__main__':
    if os.getenv("PERSPECTIVE_API_KEY"):
        safe_text = "I love this product, it's so helpful and easy to use."
        unsafe_text = "You are a stupid idiot and I hate you."
        
        safe_scores = check_text_safety(safe_text)
        print(f"'{safe_text}' -> Scores: {safe_scores}, Is Safe: {is_content_safe(safe_text)}")
        
        unsafe_scores = check_text_safety(unsafe_text)
        print(f"'{unsafe_text}' -> Scores: {unsafe_scores}, Is Safe: {is_content_safe(unsafe_text)}")
    else:
        print("Set PERSPECTIVE_API_KEY to run this example.")
