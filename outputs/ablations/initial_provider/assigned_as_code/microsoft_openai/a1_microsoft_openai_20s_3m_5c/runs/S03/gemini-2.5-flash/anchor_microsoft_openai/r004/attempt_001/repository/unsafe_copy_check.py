import os
from google.cloud import language_v1

def check_unsafe_content(text: str, project_id: str = None) -> dict:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("Google Cloud project ID not provided or found in GOOGLE_CLOUD_PROJECT environment variable.")

    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis to detect highly negative content as a proxy for 'unsafe'
    sentiment_response = client.analyze_sentiment(request={'document': document})
    sentiment = sentiment_response.document_sentiment

    # You could also analyze entities for specific keywords related to unsafe content
    # entity_response = client.analyze_entities(request={'document': document})
    # entities = entity_response.entities

    is_unsafe = False
    unsafe_reason = ""

    if sentiment.score < -0.5 and sentiment.magnitude > 1.0: # Heuristic for strong negative sentiment
        is_unsafe = True
        unsafe_reason = f"Highly negative sentiment detected (score: {sentiment.score:.2f}, magnitude: {sentiment.magnitude:.2f})."

    # In a real-world scenario, you would integrate with a dedicated content moderation API or a custom classification model.

    return {
        "is_unsafe": is_unsafe,
        "unsafe_reason": unsafe_reason,
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude
    }
