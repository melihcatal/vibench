from google.cloud import language_v1

def moderate_text_sentiment(text_content):
    """
    Moderates text content by analyzing its sentiment using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    return {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
    }

if __name__ == "__main__":
    # Example usage:
    text_to_moderate_positive = "This vendor note is excellent and highly recommend!"
    sentiment_positive = moderate_text_sentiment(text_to_moderate_positive)
    #print(f"Text: \"{text_to_moderate_positive}\"")
    #print(f"Sentiment Score: {sentiment_positive["score"]}")
    #print(f"Sentiment Magnitude: {sentiment_positive["magnitude"]}")

    text_to_moderate_negative = "The vendor delivered a terrible product with many defects."
    sentiment_negative = moderate_text_sentiment(text_to_moderate_negative)
    #print(f"Text: \"{text_to_moderate_negative}\"")
    #print(f"Sentiment Score: {sentiment_negative["score"]}")
    #print(f"Sentiment Magnitude: {sentiment_negative["magnitude"]}")
