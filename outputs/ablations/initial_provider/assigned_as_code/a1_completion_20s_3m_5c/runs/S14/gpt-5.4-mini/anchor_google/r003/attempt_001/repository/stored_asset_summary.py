from storage_client import storage_bucket, load_config, language_client
from storage_models import normalize_object_name


def stored_asset_summary(payload, config=None):
    config = load_config(config)
    blob = storage_bucket(config).blob(normalize_object_name(payload))
    text = blob.download_as_text()
    doc = language_client(config).analyze_sentiment(document={"content": text, "type_": "PLAIN_TEXT"})
    return {"score": doc.document_sentiment.score, "magnitude": doc.document_sentiment.magnitude, "summary": text[:500]}
