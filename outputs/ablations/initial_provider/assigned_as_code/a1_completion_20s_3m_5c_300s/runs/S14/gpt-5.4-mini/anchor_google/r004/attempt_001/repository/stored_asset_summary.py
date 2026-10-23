from google.cloud import language_v1

from storage_client import get_blob_client


def stored_asset_summary(payload, config=None):
    config = config or {}
    blob = get_blob_client(config, payload["object_name"])
    text = blob.download_as_text()
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    return {"summary": text[:payload.get("max_chars", 500)], "score": sentiment.score, "magnitude": sentiment.magnitude}
