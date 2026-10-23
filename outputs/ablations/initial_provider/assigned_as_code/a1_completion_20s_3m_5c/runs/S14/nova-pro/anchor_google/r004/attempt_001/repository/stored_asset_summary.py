from google.cloud import storage
from storage_client import get_storage_client
from google.cloud import language


def stored_asset_summary(payload):
    client = get_storage_client()
    blob = client.bucket(payload["bucket"]).blob(payload["object_name"])
    content = blob.download_as_text()
    client = language.LanguageServiceClient()
    document = language.Document(content=content, type_=language.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    summary = response.document_sentiment.text
    return {"summary": summary}