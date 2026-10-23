from google.cloud import language_v1


def visual_safety_text(payload, config=None):
    client = language_v1.LanguageServiceClient()
    text = payload.get("text", "")
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    return {"unsafe": response.document_sentiment.score < float((config or {}).get("threshold", -0.5))}
