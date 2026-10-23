from google.cloud import language_v1


def analyze_sentiment_for_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Perform sentiment analysis to get a score and magnitude
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    # For content safety, we can define a simple heuristic:
    # - A very negative score might indicate potentially unsafe content.
    # - A high magnitude indicates the strength of emotion, regardless of positive or negative.
    # More sophisticated safety checks would involve entity extraction, content classification, etc.
    # This is a basic example using sentiment as a proxy.

    is_potentially_unsafe = False
    safety_score_threshold = -0.5  # Example threshold for considering content potentially unsafe
    safety_magnitude_threshold = 1.0  # Example threshold for strong emotion

    if sentiment.score < safety_score_threshold and sentiment.magnitude > safety_magnitude_threshold:
        is_potentially_unsafe = True

    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "is_potentially_unsafe": is_potentially_unsafe,
        "message": "Content is potentially unsafe based on sentiment." if is_potentially_unsafe else "Content appears safe based on sentiment."
    }


def classify_text_for_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify text into categories to infer safety
    # This requires enabling the Text Classification API in Google Cloud and potentially training a custom model
    # For demonstration, we'll use the pre-trained model for general categories.
    # This is a more direct approach to content safety than just sentiment.

    try:
        response = client.classify_text(request={'document': document})
        categories = [{
            "name": category.name,
            "confidence": category.confidence
        } for category in response.categories]
        
        # Simple check for categories that might indicate unsafe content
        is_potentially_unsafe = any(
            "/Self-harm" in c["name"] or 
            "/Violence" in c["name"] or 
            "/Illicit Goods" in c["name"]
            for c in categories
        )

        return {
            "categories": categories,
            "is_potentially_unsafe": is_potentially_unsafe,
            "message": "Content is potentially unsafe based on classification." if is_potentially_unsafe else "Content appears safe based on classification."
        }
    except Exception as e:
        return {"error": str(e), "message": "Text classification failed, ensure API is enabled and text is sufficient."}
