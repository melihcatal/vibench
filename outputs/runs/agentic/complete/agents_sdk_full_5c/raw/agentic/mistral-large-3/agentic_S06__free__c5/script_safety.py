from google.cloud import language_v1

def check_script_safety(text: str) -> dict:
    """
    Checks narration scripts for unsafe content using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(
        request={"document": document}
    )
    
    # Check for toxic content using sentiment magnitude as a proxy
    toxicity_score = response.document_sentiment.magnitude
    
    return {
        "is_safe": toxicity_score < 2.0,
        "toxicity_score": toxicity_score,
        "sentiment_score": response.document_sentiment.score
    }