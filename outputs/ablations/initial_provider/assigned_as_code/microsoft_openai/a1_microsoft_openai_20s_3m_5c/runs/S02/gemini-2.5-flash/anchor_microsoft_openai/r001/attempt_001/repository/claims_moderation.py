from google.cloud import language_v1
from identity_client import get_google_cloud_config

def moderate_text_claim(text_content: str) -> dict:
    gcp_config = get_google_cloud_config()
    # Project ID is generally handled by the environment or service account for Google Cloud APIs

    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Analyze sentiment
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    
    # Classify content (requires a custom classification model for specific moderation tasks, 
    # but we can use general categories for demonstration)
    # For a more robust moderation, specific content categories or a custom model would be needed.
    # For this example, we'll just get general categories if available.
    try:
        classify_response = client.classify_text(request={'document': document})
        categories = [category.name for category in classify_response.categories]
    except Exception: # Catching a general exception as classify_text might not always return categories for short/simple texts
        categories = []

    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "categories": categories,
    }
