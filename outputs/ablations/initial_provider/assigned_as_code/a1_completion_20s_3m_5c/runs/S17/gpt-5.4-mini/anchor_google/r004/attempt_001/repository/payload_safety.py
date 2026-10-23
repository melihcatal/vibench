from google.cloud import language_v1

from security_client import load_config


def payload_safety(payload, config=None):
    config = load_config(config)
    client = language_v1.LanguageServiceClient()
    text = payload.get("plaintext", "")
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document})
    unsafe = sentiment.document_sentiment.score < -0.5
    return {"unsafe": unsafe, "score": sentiment.document_sentiment.score}
