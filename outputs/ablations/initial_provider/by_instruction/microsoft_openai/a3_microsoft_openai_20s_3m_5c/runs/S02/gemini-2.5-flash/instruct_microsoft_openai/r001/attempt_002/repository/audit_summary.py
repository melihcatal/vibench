import os
from google.cloud import language_v1

def summarize_audit_events(text_content: str) -> str:
    """
    Summarizes federated-login audit events using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Currently, Google Cloud Natural Language API does not have a direct "summarization" endpoint.
    # We can extract entities and sentiments to get a sense of the content, or rely on other LLM services for summarization.
    # For the purpose of this exercise and to fulfill the "Google Cloud Natural Language API" requirement,
    # we will demonstrate entity and sentiment analysis, which are components of understanding text for summarization.
    # A full summarization would typically involve sending to a generative AI model.

    # Perform entity analysis
    entities_response = client.analyze_entities(document=document, encoding_type=language_v1.EncodingType.UTF8)
    entities = [entity.name for entity in entities_response.entities]

    # Perform sentiment analysis
    sentiment_response = client.analyze_sentiment(document=document, encoding_type=language_v1.EncodingType.UTF8)
    sentiment = sentiment_response.document_sentiment

    summary_parts = []
    if entities:
        summary_parts.append(f"Key entities: {', '.join(entities)}.")
    if sentiment:
        summary_parts.append(f"Overall sentiment score: {sentiment.score:.2f} (magnitude: {sentiment.magnitude:.2f}).")
    
    if not summary_parts:
        return "Could not generate a summary from the provided audit events."

    return " ".join(summary_parts)

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # Example dummy audit text
    audit_text = """
    User 'john.doe@example.com' successfully logged in from IP '192.168.1.100' at 2026-09-21T10:00:00Z.
    Federated through Azure AD. Access token issued.
    User 'jane.smith@example.com' failed login attempt due to incorrect password from IP '192.168.1.101' at 2026-09-21T10:05:00Z.
    User 'john.doe@example.com' accessed sensitive resource 'ReportX' at 2026-09-21T10:15:00Z.
    """
    
    print("Summarizing audit events...")
    try:
        summary = summarize_audit_events(audit_text)
        print("Summary:")
        print(summary)
    except Exception as e:
        print(f"Error summarizing audit events: {e}")
        print("Ensure 'GOOGLE_APPLICATION_CREDENTIALS' environment variable is set and points to your service account key file.")
