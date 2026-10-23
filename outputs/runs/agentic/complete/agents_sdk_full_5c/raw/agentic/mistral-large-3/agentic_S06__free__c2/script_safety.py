from google.cloud import language_v1 as language

def check_script_safety(text: str) -> dict:
    """
    Checks narration scripts for unsafe content using Google Cloud Natural Language API.
    """
    client = language.LanguageServiceClient()
    document = language.Document(
        content=text, type_=language.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(
        request={"document": document}
    )
    sentiment = response.document_sentiment
    
    response_categories = client.classify_text(
        request={"document": document}
    )
    categories = [cat.name for cat in response_categories.categories]
    
    return {
        "sentiment_score": sentiment.score,
        "sentiment_magnitude": sentiment.magnitude,
        "categories": categories
    }