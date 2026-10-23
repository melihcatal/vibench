import os
from google.cloud import language_v1
from typing import List, Dict, Any

# Google Cloud Natural Language API Configuration
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or authenticate using other methods supported by google-cloud-python SDK.

def moderate_text_claims(text_content: str) -> Dict[str, Any]:
    """
    Moderates free-text claims or notes using Google Cloud Natural Language API.
    Analyzes sentiment and categorizes content.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Analyze sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # Classify content into categories
    # This feature requires billing to be enabled on the Google Cloud project.
    # For this example, we'll include it but it might return empty if not configured.
    try:
        response = client.classify_text(request={'document': document})
        categories = [{'name': category.name, 'confidence': category.confidence} for category in response.categories]
    except Exception as e:
        print(f"Warning: Could not classify text (billing might not be enabled): {e}")
        categories = []

    moderation_results = {
        "text": text_content,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "categories": categories
    }

    return moderation_results

if __name__ == "__main__":
    # Example usage
    sample_claim = "This user seems to be very happy with their experience, which is great!"
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file.
    # results = moderate_text_claims(sample_claim)
    # print(f"Moderation Results for \""""" {sample_claim}""""":")
    # print(json.dumps(results, indent=2))

    print("To test, ensure GOOGLE_APPLICATION_CREDENTIALS is set and call moderate_text_claims.")
