from observability_client import ObservabilityClient
from google.cloud.language_v1 import Document, DocumentSentiment, Sentiment, AnnotateTextRequest

def check_log_text_safety(log_message_text, config=None):
    config = config or {}
    client = ObservabilityClient(project_id=config["project_id"])
    nl_client = client.get_natural_language_client()

    document = Document(content=log_message_text, type=Document.Type.PLAIN_TEXT)
    
    # Perform sentiment analysis and entity analysis as a proxy for safety
    # For true safety, more advanced methods or specific safety APIs might be needed.
    response = nl_client.annotate_text(document=document, features={'extract_syntax': False, 'extract_entities': True, 'extract_document_sentiment': True})

    sentiment_score = response.document_sentiment.score
    sentiment_magnitude = response.document_sentiment.magnitude
    
    unsafe_keywords = ["malicious", "attack", "exploit", "vulnerability", "hack"]
    is_unsafe_keyword_present = any(keyword in log_message_text.lower() for keyword in unsafe_keywords)

    # Simple heuristic for safety: highly negative sentiment or presence of unsafe keywords
    is_unsafe = (sentiment_score < -0.5 and sentiment_magnitude > 1.0) or is_unsafe_keyword_present

    return {
        "log_message": log_message_text,
        "is_unsafe": is_unsafe,
        "sentiment_score": sentiment_score,
        "sentiment_magnitude": sentiment_magnitude,
        "contains_unsafe_keywords": is_unsafe_keyword_present,
    }
