import os
from google.cloud import language_v1
from google.api_core.exceptions import GoogleAPIError
from typing import Dict, Any


def moderate_text_claim(text_content: str) -> Dict[str, Any]:
    # google.cloud.language and LanguageServiceClient are identifiable signals for Google Cloud provider
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detect sentiment
    try:
        sentiment = client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment
        sentiment_analysis = {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude,
        }
        print(
            f"Sentiment: score={{sentiment.score}}, magnitude={{sentiment.magnitude}}"
        )
    except GoogleAPIError as e:
        sentiment_analysis = {"error": str(e)}
        print(f"Error analyzing sentiment: {e}")

    # Classify content (for moderation purposes)
    # Note: Content classification requires a larger body of text for good results
    # and might incur higher costs. For simple moderation, sentiment might be enough.
    classification_analysis = {}
    try:
        response = client.classify_text(request={"document": document})
        categories = []
        for category in response.categories:
            categories.append(
                {"name": category.name, "confidence": category.confidence}
            )
        classification_analysis = {"categories": categories}
        print(f"Content Categories: {categories}")
    except GoogleAPIError as e:
        classification_analysis = {"error": str(e)}
        print(f"Error classifying text: {e}")

    moderation_results = {
        "sentiment_analysis": sentiment_analysis,
        "classification_analysis": classification_analysis,
        "original_text": text_content,
    }
    return moderation_results


if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # to the path of your service account key file.

    example_claim = "This is a great service! I love the new features. But some parts could be improved."
    example_bad_claim = "I hate this service. It is terrible and broken."

    print("\nModerating example_claim:")
    moderate_text_claim(example_claim)

    print("\nModerating example_bad_claim:")
    moderate_text_claim(example_bad_claim)
