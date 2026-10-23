import os
from google.cloud import language_v1
from typing import Dict, Any


def moderate_text_with_google_nl(
    text_content: str, language_code: str = "en"
) -> Dict[str, Any]:
    """
    Analyzes text content for sentiment and entities using Google Cloud Natural Language API
    to help with moderation decisions for free-text claims or notes.

    This function specifically demonstrates sentiment analysis, which can be a component
    of moderation (e.g., flagging highly negative content).
    For full content moderation, one would typically use additional services or more advanced
    analysis of entities and categories.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language=language_code,
    )

    # Perform sentiment analysis
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    # You could also perform entity analysis or content classification for more comprehensive moderation
    # entities = client.analyze_entities(request={'document': document}).entities
    # moderation_categories = client.classify_text(request={'document': document}).categories

    return {
        "text_content": text_content,
        "sentiment": {"score": sentiment.score, "magnitude": sentiment.magnitude},
        # Add other analysis results here as needed
    }


if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # pointing to your service account key file.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print(
            "WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. Google NL API calls may fail."
        )

    example_claims = [
        "This is a perfectly normal user claim, nothing to worry about here.",
        "I am extremely unhappy with the service, it's absolutely terrible!",
        "Great experience, highly recommend!",
        "This user mentioned something about a 'bomb' in their notes. Needs review.",
    ]

    print("Moderating example claims with Google Cloud Natural Language API...")
    for i, claim in enumerate(example_claims):
        print(f"\n--- Claim {i + 1} ---")
        print(f"Text: {claim}")
        try:
            moderation_result = moderate_text_with_google_nl(claim)
            print(f"Sentiment Score: {moderation_result['sentiment']['score']:.2f}")
            print(
                f"Sentiment Magnitude: {moderation_result['sentiment']['magnitude']:.2f}"
            )
            # Basic moderation logic: flag if sentiment is very negative
            if (
                moderation_result["sentiment"]["score"] < -0.5
                and moderation_result["sentiment"]["magnitude"] > 1.0
            ):
                print("MODERATION ALERT: Highly negative sentiment detected.")
        except Exception as e:
            print(f"Error moderating claim: {e}")
