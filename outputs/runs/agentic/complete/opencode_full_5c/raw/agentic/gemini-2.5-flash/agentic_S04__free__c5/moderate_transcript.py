import os
import sys
from google.cloud import language_v1
from typing import List, Dict, Any


def moderate_text_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyzes the sentiment of the provided text using Google Cloud Natural Language API
    as a basic form of moderation.

    Args:
        text: The text to moderate.

    Returns:
        A dictionary containing sentiment score and magnitude.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # The actual sentiment analysis happens here
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    result = {"score": sentiment.score, "magnitude": sentiment.magnitude, "summary": ""}

    if sentiment.score < -0.25:
        result["summary"] = "Potentially negative or critical content detected."
    elif sentiment.score > 0.25:
        result["summary"] = "Potentially positive content detected."
    else:
        result["summary"] = "Neutral content detected."

    print(f"Moderation (Sentiment) for: '{text}'")
    print(f"  Score: {result['score']:.2f}, Magnitude: {result['magnitude']:.2f}")
    print(f"  Summary: {result['summary']}")

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python moderate_transcript.py <text_to_moderate>")
        print(
            'Example: python moderate_transcript.py "I hate this product, it is terrible."'
        )
        sys.exit(1)

    text_to_moderate = " ".join(sys.argv[1:])

    # For demonstration, ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    try:
        moderation_result = moderate_text_sentiment(text_to_moderate)
        print("\n--- Moderation Results ---")
        print(f"Sentiment Score: {moderation_result['score']}")
        print(f"Sentiment Magnitude: {moderation_result['magnitude']}")
        print(f"Moderation Summary: {moderation_result['summary']}")
    except Exception as e:
        print(f"Error moderating text: {e}")
        sys.exit(1)
