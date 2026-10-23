from google.cloud import storage
from google.cloud import language_v1

from storage_client import get_bucket
from storage_models import DocumentInsight, normalize_object_name


def stored_asset_summary(bucket_name: str, object_name: str) -> dict:
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(normalize_object_name(object_name))
    text = blob.download_as_text()
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.summarize_text(request={"document": document})
    summary = response.summary.text if hasattr(response, "summary") and response.summary else None
    return DocumentInsight(bucket=bucket_name, name=blob.name, text=text, summary=summary).to_dict()
