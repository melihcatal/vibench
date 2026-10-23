from google.cloud import storage
from storage_client import get_storage_client
from google.cloud import language


def asset_metadata_embedding(payload):
    client = get_storage_client()
    blob = client.bucket(payload["bucket"]).blob(payload["object_name"])
    content = blob.download_as_text()
    client = language.LanguageServiceClient()
    document = language.Document(content=content, type_=language.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    embedding = response.document_sentiment.score
    return {"embedding": embedding}