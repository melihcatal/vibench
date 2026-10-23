from google.cloud import language_v1
from speech_models import ModerationRequest


def moderate_transcript_text(request: ModerationRequest) -> dict:
    """Moderates transcript text using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=request.text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # You can choose different features for analysis:
    # sentiment, entities, entity_sentiment, syntax, classify_text
    response = client.analyze_sentiment(document=document)

    # For content classification:
    # response = client.classify_text(document=document)

    # Return a dictionary with relevant moderation results
    # This is a simplified example, a real moderation would involve more specific analysis
    return {
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude,
    }
