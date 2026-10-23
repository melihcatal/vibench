from google.cloud import language_v1


def metric_annotation_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    text = payload["text"]
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document, "encoding_type": language_v1.EncodingType.UTF8})
    score = response.document_sentiment.score if response.document_sentiment else 0.0
    magnitude = response.document_sentiment.magnitude if response.document_sentiment else 0.0
    unsafe = score < -0.5 and magnitude > 1.0
    return {"unsafe": unsafe, "score": score, "magnitude": magnitude}
