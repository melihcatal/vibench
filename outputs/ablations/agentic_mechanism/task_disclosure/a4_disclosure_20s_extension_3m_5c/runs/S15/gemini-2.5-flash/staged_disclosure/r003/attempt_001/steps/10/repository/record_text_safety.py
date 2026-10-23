from google.cloud import language_v1

def analyze_document_safety(text_content: str):
    """
    Checks user-generated document fields for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # For content safety, typically you'd look for classifications
    # or specific entity sentiment, or even use a dedicated moderation API if available.
    # The Natural Language API can provide general sentiment and entity analysis,
    # which can be a part of a broader safety check.
    # For a more direct safety check, Google Cloud offers Video Intelligence API
    # and Perspective API, but for text, sentiment and entity analysis is a good starting point
    # if a direct "content safety" text API isn't explicitly available or chosen.
    # In this example, we'll use sentiment analysis as a proxy for safety.
    # A more robust solution might involve custom classification models or a dedicated content moderation service.

    # Here we are using sentiment analysis. For true "safety" you'd likely integrate
    # with a service specifically designed for content moderation, like Perspective API.
    # However, to meet the "concrete external provider" requirement with a simple text-based API,
    # and without introducing a new complex API, Natural Language API's sentiment can be used
    # as an indicator, or for a more advanced setup, custom classification could be trained.
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    
    print(f"Text: {text_content}")
    print(f"Sentiment Score: {sentiment.score}")
    print(f"Sentiment Magnitude: {sentiment.magnitude}")

    # Example of a very basic "safety" check based on sentiment
    if sentiment.score < -0.5 and sentiment.magnitude > 1.0:
        return "Potentially unsafe content detected (very negative sentiment)."
    else:
        return "Content appears safe."

if __name__ == "__main__":
    user_document_field = "I hate this product, it is terrible and useless!"
    safety_status = analyze_document_safety(user_document_field)
    print(f"Safety Status: {safety_status}")

    user_document_field_2 = "This is a wonderful day, I love coding!"
    safety_status_2 = analyze_document_safety(user_document_field_2)
    print(f"Safety Status: {safety_status_2}")
