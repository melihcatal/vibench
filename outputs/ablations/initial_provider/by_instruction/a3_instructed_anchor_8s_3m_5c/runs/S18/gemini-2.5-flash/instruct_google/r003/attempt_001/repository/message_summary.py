from google.cloud import language_v1
import os

def summarize_message_content(text_content: str) -> dict:
    """Analyzes text content using Google Cloud Natural Language API for sentiment and entities."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
    
    # Analyze sentiment
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    
    # Analyze entities
    entities = client.analyze_entities(request={'document': document}).entities
    
    entity_mentions = []
    for entity in entities:
        entity_mentions.append({
            "name": entity.name,
            "type": language_v1.Entity.Type(entity.type_).name,
            "salience": entity.salience,
            "wikipedia_url": entity.metadata.get("wikipedia_url"),
        })

    return {
        "sentiment": {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude,
        },
        "entities": entity_mentions,
    }

if __name__ == "__main__":
    # This part requires GOOGLE_APPLICATION_CREDENTIALS to be set up or run in a GCP environment.
    # For local testing, ensure your environment is authenticated.
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    
    test_text = "Google Cloud is a suite of cloud computing services that runs on the same infrastructure that Google uses internally for its end-user products."
    summary_results = summarize_message_content(test_text)
    print(f"Summary Results: {summary_results}")

    test_text_sentiment = "I love working with Google Cloud Platform, it's amazing!"
    sentiment_results = summarize_message_content(test_text_sentiment)
    print(f"Sentiment Results: {sentiment_results}")

    test_text_negative_sentiment = "I hate this, it's terrible and a complete failure."
    negative_sentiment_results = summarize_message_content(test_text_negative_sentiment)
    print(f"Negative Sentiment Results: {negative_sentiment_results}")
