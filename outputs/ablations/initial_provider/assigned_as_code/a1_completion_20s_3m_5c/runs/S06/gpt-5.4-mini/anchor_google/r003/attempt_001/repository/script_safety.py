from google.cloud import language_v1


def script_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=payload["text"], type_=language_v1.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(request={"document": document})
    score = analysis.document_sentiment.score
    return {"safe": score >= float((config or {}).get("min_sentiment", -0.5)), "sentiment_score": score}
