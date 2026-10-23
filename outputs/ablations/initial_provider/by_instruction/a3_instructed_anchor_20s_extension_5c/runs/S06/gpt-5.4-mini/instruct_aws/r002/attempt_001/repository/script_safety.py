from google.cloud import language_v1


def check_script_safety(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    score = response.document_sentiment.score if response.document_sentiment else 0.0
    magnitude = response.document_sentiment.magnitude if response.document_sentiment else 0.0
    return {"safe": score >= -0.5, "sentiment_score": score, "sentiment_magnitude": magnitude}
