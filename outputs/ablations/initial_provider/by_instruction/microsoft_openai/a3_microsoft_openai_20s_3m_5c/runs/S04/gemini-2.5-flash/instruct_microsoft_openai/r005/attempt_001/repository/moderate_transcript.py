import os
from typing import List, Dict, Any
from google.cloud import language_v1

def moderate_transcript_text(text: str, project_id: str) -> Dict[str, Any]:
    """
    Moderates transcript text using Google Cloud Natural Language API's classification
    and sentiment analysis.

    Args:
        text: The text segment to moderate.
        project_id: Your Google Cloud project ID.

    Returns:
        A dictionary containing content categories and sentiment analysis results.
    """
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided.")

    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    moderation_results = {}

    # Perform content classification to identify potentially sensitive categories
    try:
        classification_response = client.classify_text(request={"document": document})
        categories = []
        for category in classification_response.categories:
            categories.append({"name": category.name, "confidence": category.confidence})
        moderation_results["categories"] = categories
        print(f"Classified text into categories: {categories}")
    except Exception as e:
        print(f"Could not perform text classification: {e}")
        moderation_results["categories"] = []

    # Perform sentiment analysis as another signal for moderation (e.g., highly negative sentiment)
    try:
        sentiment_response = client.analyze_sentiment(request={"document": document})
        sentiment = sentiment_response.document_sentiment
        moderation_results["sentiment"] = {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude
        }
        print(f"Sentiment: Score={sentiment.score}, Magnitude={sentiment.magnitude}")
    except Exception as e:
        print(f"Could not perform sentiment analysis: {e}")
        moderation_results["sentiment"] = None

    return moderation_results

if __name__ == "__main__":
    # Example Usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate your gcloud CLI.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # gcloud auth application-default login

    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # Or replace with your actual project ID
    # if not project_id:
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace with your project ID.")
    # else:
    #     text_to_moderate = (
    #         "The quick brown fox jumps over the lazy dog. This is a normal sentence."
    #         "However, this next part contains some violent and hateful speech that should be flagged."
    #         "Another sentence about a happy cat."
    #     )
    #     print(f"Moderating text:\n'{text_to_moderate}'\n")
    #     try:
    #         results = moderate_transcript_text(text_to_moderate, project_id)
    #         print("\nModeration Results:")
    #         print(json.dumps(results, indent=2))
    #     except Exception as e:
    #         print(f"Error during moderation: {e}")
    print("To run this example, set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables and uncomment the test lines.")
