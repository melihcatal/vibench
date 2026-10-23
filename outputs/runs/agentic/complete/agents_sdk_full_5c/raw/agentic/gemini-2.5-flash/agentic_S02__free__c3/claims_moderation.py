from google.cloud import language_v1
from typing import Dict, Any

from identity_client import GOOGLE_CLOUD_PROJECT_ID

def moderate_text_claims(text: str) -> Dict[str, Any]:
    """
    Moderates free-text claims or notes using Google Cloud Natural Language API
    to assess sentiment and content classification.

    Args:
        text: The free-text claim or note to moderate.

    Returns:
        A dictionary containing sentiment score, magnitude, and content classification categories.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Analyze sentiment
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Classify text content
    # Note: Classification requires a minimum text length to be effective.
    # It might return empty categories for very short or non-categorizable texts.
    try:
        response_classify = client.classify_text(request={'document': document})
        categories = [{'name': cat.name, 'confidence': cat.confidence} for cat in response_classify.categories]
    except Exception as e:
        # Handle cases where classification might fail or return no categories
        print(f"Warning: Could not classify text (may be too short or generic): {e}")
        categories = []

    moderation_results = {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "content_categories": categories,
    }
    return moderation_results

if __name__ == "__main__":
    test_claim_positive = "This is a fantastic user experience! I loved it."
    test_claim_negative = "Terrible service, very disappointed and frustrated."
    test_claim_neutral = "The user logged in successfully and updated their profile."
    test_claim_mixed = "The login was fast, but the profile update was slow."

    print(f"\nModerating: \"{test_claim_positive}\"\n")
    print(moderate_text_claims(test_claim_positive))

    print(f"\nModerating: \"{test_claim_negative}\"\n")
    print(moderate_text_claims(test_claim_negative))

    print(f"\nModerating: \"{test_claim_neutral}\"\n")
    print(moderate_text_claims(test_claim_neutral))
    
    print(f"\nModerating: \"{test_claim_mixed}\"\n")
    print(moderate_text_claims(test_claim_mixed))
