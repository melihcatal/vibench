from google.cloud import language_v1
import os

def summarize_moderation_decision(text_content):
    """Summarizes moderation decisions using Google Cloud Natural Language API."""

    # Initialize the Google Cloud Natural Language client
    # The client library import and client initialization make the provider identifiable.
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # You can use analyze_sentiment as a basic moderation proxy to see if text is negative
    # or classify_text for more advanced content categorization if you have a custom model.
    # For this example, we'll use sentiment as a simple demonstration.

    try:
        sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
        
        summary = {
            "text": text_content,
            "sentiment_score": sentiment.score,
            "sentiment_magnitude": sentiment.magnitude,
            "moderation_suggestion": "Review needed" if sentiment.score < -0.2 else "Likely acceptable"
        }
        return summary
    except Exception as e:
        return {"error": str(e), "text": text_content, "moderation_suggestion": "API call failed"}

if __name__ == '__main__':
    # Example usage:
    text_to_moderate_positive = "This is a wonderful and positive message!"
    text_to_moderate_negative = "I hate this content, it's terrible and offensive."
    text_to_moderate_neutral = "This is a neutral statement about a topic."

    print("Moderation Summary (Positive):", summarize_moderation_decision(text_to_moderate_positive))
    print("Moderation Summary (Negative):", summarize_moderation_decision(text_to_moderate_negative))
    print("Moderation Summary (Neutral):", summarize_moderation_decision(text_to_moderate_neutral))
