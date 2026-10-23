from google.cloud import language_v1
from storage_client import get_storage_client, get_bucket_name


def summarize_stored_asset(object_name: str) -> str:
    """
    Summarize content extracted from a stored asset using Google Cloud Natural Language API.
    
    Args:
        object_name: Name of the object in the bucket (assumed to contain text).
        
    Returns:
        Summary of the content.
    """
    client = language_v1.LanguageServiceClient()
    bucket_name = get_bucket_name()
    
    # Fetch the object content
    bucket = get_storage_client().bucket(bucket_name)
    blob = bucket.blob(object_name)
    text = blob.download_as_text()
    
    # Analyze the text for summary
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_entities(request={"document": document})
    
    # Simple summary: top entities
    summary = " ".join(
        entity.name for entity in sorted(
            response.entities, key=lambda e: e.salience, reverse=True
        )[:5]
    )
    
    return summary